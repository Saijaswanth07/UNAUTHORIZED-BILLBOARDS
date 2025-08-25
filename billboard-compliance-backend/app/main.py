from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, crud, auth
from .database import engine, get_db
from .config import settings
import uvicorn

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Billboard Compliance API")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(crud.router, prefix="/api", tags=["Core Operations"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Billboard Compliance API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
