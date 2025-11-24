from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, users, documents, ingest, email
from app.database import Base, engine
from app.models import user, document  # ensure models are imported so tables are created

# Initialize FastAPI app
app = FastAPI(
    title="DocuMagic API",
    version="1.0.0",
    description="Backend for document ingestion, parsing, metadata extraction and storage."
)

# CORS setup (allows frontend like React/Vue to talk to API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # TODO: restrict origins in production
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
app.include_router(auth.router)
app.include_router(email.router, prefix="/email", tags=["Email"])   # Zoho Mail integration

# Create tables when app starts
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
