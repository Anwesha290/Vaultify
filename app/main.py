from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime,timezone
import os
from pathlib import Path

from app.routes import router

# Initialize FastAPI app
app = FastAPI(
    title="Vaultify",
    description="Secure one-time secret sharing API",
    version="1.0.0"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = Path(__file__).parent.parent / "static"
static_dir.mkdir(exist_ok=True, parents=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Set up templates
templates_dir = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=templates_dir)
templates.env.globals.update({
    'now': datetime.now(timezone.utc)
})

# Include API routes
app.include_router(router, prefix="/api")

# Serve frontend
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/view/{secret_id}", response_class=HTMLResponse)
async def view_secret_page(secret_id: str, request: Request):
    return templates.TemplateResponse("view_secret.html", {
        "request": request,
        "secret_id": secret_id
    })
