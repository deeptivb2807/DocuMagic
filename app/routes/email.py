from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.email_ingestion import ZohoMailClient

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/emails")
def get_emails(limit: int = 5, owner_id: int = 1, db: Session = Depends(get_db)):
    """
    Fetch recent emails from Zoho Mail inbox and store attachments in DB.
    """
    zoho_client = ZohoMailClient()
    emails = zoho_client.fetch_emails(limit=limit, db=db, owner_id=owner_id)
    return {"emails": emails}
