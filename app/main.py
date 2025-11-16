from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth

# Import routers (we will create them gradually)
from app.routes import users, documents, ingest

app = FastAPI(
    title="DocuMagic API",
    version="1.0.0",
    description="Backend for document ingestion, parsing, metadata extraction and storage."
)

# CORS setup (allows frontend like React/Vue to talk to API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # update later for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def home():
    return {"message": "DocuMagic API is running..."}

# Register routers (endpoints)
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(ingest.router, prefix="/ingest", tags=["Ingestion"])

from app.database import Base, engine
from app.models import user, document

# Create tables when app starts
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)