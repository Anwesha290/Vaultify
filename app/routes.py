from fastapi import APIRouter, HTTPException, Response
from uuid import uuid4
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import JSONResponse

from app.db import collection
from app.encryption import encrypt_secret, decrypt_secret

router = APIRouter()

class SecretIn(BaseModel):
    secret: str
    max_views: int = 1
    expire_seconds: int = 120  # 2 minutes default

import logging

logger = logging.getLogger(__name__)

@router.post("/create-secret")
async def create_secret(data: SecretIn):
    try:
        logger.info(f"Creating secret with max_views={data.max_views}, expire_seconds={data.expire_seconds}")
        
        uid = str(uuid4())
        logger.debug(f"Generated secret ID: {uid}")
        
        encrypted = encrypt_secret(data.secret)
        logger.debug("Secret encrypted successfully")
        
        expiry = datetime.now(timezone.utc) + timedelta(seconds=data.expire_seconds)
        logger.debug(f"Secret will expire at: {expiry}")

        # Prepare the document to insert
        secret_doc = {
            "_id": uid,
            "secret": encrypted,
            "expiry": expiry,
            "views": 0,
            "max_views": data.max_views,
            "created_at": datetime.now(timezone.utc)
        }
        
        logger.debug(f"Inserting document into database: {secret_doc}")
        
        # Insert the secret into the database
        result = collection.insert_one(secret_doc)
        logger.info(f"Insert result: {result.inserted_id}")
        
        # Verify the document was inserted
        if not result.inserted_id:
            logger.error("Failed to insert document into database")
            raise HTTPException(status_code=500, detail="Failed to create secret")

        if not result.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to create secret")

        # Return the secret ID (not the full URL, let frontend construct it)
        return {"id": uid}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while creating the secret: {str(e)}"
        )


@router.get("/get-secret/{secret_id}")
async def get_secret(secret_id: str):
    try:
        # Find the secret
        doc = collection.find_one({"_id": secret_id})
        
        if not doc:
            raise HTTPException(status_code=404, detail="Secret not found or already viewed")
        
        now_utc = datetime.now(timezone.utc)
        
        # Make expiry timezone-aware if it isn't already
        expiry = doc["expiry"]
        if expiry.tzinfo is None:
            expiry = expiry.replace(tzinfo=timezone.utc)

        # Check if secret has expired
        if now_utc > expiry:
            collection.delete_one({"_id": secret_id})
            raise HTTPException(status_code=410, detail="This secret has expired")

        # Check max views
        current_views = doc["views"] + 1  # Increment view count
        max_views = doc["max_views"]
        
        # Decrypt the secret before deleting (if it's the last view)
        decrypted = decrypt_secret(doc["secret"])
        
        # Update or delete based on view count
        if current_views >= max_views:
            # Delete if this is the last view
            collection.delete_one({"_id": secret_id})
        else:
            # Update view count
            collection.update_one(
                {"_id": secret_id},
                {"$set": {"views": current_views}}
            )
        
        # Calculate time remaining in seconds
        time_remaining = int((expiry - now_utc).total_seconds())
        
        return {
            "secret": decrypted,
            "views_remaining": max(0, max_views - current_views),
            "expires_in_seconds": time_remaining
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while retrieving the secret: {str(e)}"
        )
    