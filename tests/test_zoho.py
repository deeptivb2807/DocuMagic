# integration_test_zoho_mail_client.py
import pytest
from app.services.email_ingestion import ZohoMailClient

@pytest.fixture
def client():
    return ZohoMailClient()

def test_send_email_real(client):
    """Actually send an email via Zoho SMTP"""
    # ⚠️ This will send a real email. Use a safe test address.
    to_address = client.email_address  # send to yourself for testing
    subject = "Integration Test Email"
    body = "This is a real test email sent by ZohoMailClient."

    result = client.send_email(to_address, subject, body)
    assert result is True

def test_fetch_emails_real(client):
    """Actually fetch emails from Zoho IMAP inbox"""
    emails = client.fetch_emails(limit=2)
    assert isinstance(emails, list)
    assert len(emails) > 0

    # Check that the first email has expected keys
    email_data = emails[0]
    assert "from" in email_data
    assert "subject" in email_data
    assert "date" in email_data
    assert "body" in email_data
    assert "attachments" in email_data
