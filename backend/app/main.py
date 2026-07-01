# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .routes import clients, appointments
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Agency API", version="1.0")

# CORS – allow your Astro dev origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clients.router)

@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/health")
async def health():
    return {"status": "ok"}

...
app.include_router(appointments.router)