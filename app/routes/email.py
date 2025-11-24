from fastapi import APIRouter
from app.services.email_ingestion import ZohoMailClient

router = APIRouter()

@router.get("/emails")
def get_emails(limit: int = 5):
    """
    Fetch recent emails from Zoho Mail inbox.
    """
    zoho_client = ZohoMailClient()
    emails = zoho_client.fetch_emails(limit=limit)
    return {"emails": emails}

@router.post("/send-email")
def send_email(to: str, subject: str, body: str):
    """
    Send an email via Zoho Mail SMTP.
    """
    zoho_client = ZohoMailClient()
    zoho_client.send_email(to_address=to, subject=subject, body=body)
    return {"status": f"Email sent to {to}"}
