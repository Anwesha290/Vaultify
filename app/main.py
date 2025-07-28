from fastapi import FastAPI
from app.routes import router
# The route = WHERE the request is sent (like the counter or address)
# The endpoint = WHAT FUNCTION handles that request (the action taken)

#this is the metadata that whill show up in swagger UI
#This is just for the web app
app = FastAPI(
    title="Vaultify",
    description="Secure one-time secret sharing API",
    version="1.0.0"
)

#This line is taking all the route definitions from routes.py and 
#adding them to the fastapi app.
app.include_router(router)
