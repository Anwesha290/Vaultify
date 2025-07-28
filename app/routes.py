from fastapi import APIRouter, HTTPException
from uuid import uuid4
from datetime import datetime, timedelta
from app.models import SecretIn
from app.db import collection
from app.encryption import encrypt_secret, decrypt_secret

router = APIRouter()

@router.post("/create-secret")
def create_secret(data: SecretIn):
    uid = str(uuid4())  # Generate a unique ID for the secret
    encrypted = encrypt_secret(data.secret)
    expiry = datetime.utcnow() + timedelta(seconds=data.expire_seconds)

    collection.insert_one({
        "_id": uid,
        "secret": encrypted,
        "expiry": expiry,
        "views": 0,
        "max_views": data.max_views
    })

    return {"link": f"http://localhost:8000/get-secret/{uid}"}


@router.get("/get-secret/{secret_id}")
def get_secret(secret_id: str):
    doc = collection.find_one({"_id": secret_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Secret not found or expired")

    if doc["views"] >= doc["max_views"]:
        collection.delete_one({"_id": secret_id})
        raise HTTPException(status_code=403, detail="Secret already viewed")

    decrypted = decrypt_secret(doc["secret"])
    collection.update_one({"_id": secret_id}, {"$inc": {"views": 1}})

    # Delete if max views reached
    if doc["views"] + 1 >= doc["max_views"]:
        collection.delete_one({"_id": secret_id})

    return {"secret": decrypted}
