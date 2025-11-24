# tests/test_zoho_client_integration.py
import unittest
from app.services.email_ingestion import ZohoMailClient


class TestZohoMailClientIntegration(unittest.TestCase):
    def setUp(self):
        # This will load settings from your .env file
        self.client = ZohoMailClient()

    def test_fetch_emails(self):
        """Fetch emails from Zoho inbox using real credentials"""
        emails = self.client.fetch_emails(limit=2)
        self.assertIsInstance(emails, list)
        # If there are emails, check structure
        if emails:
            email_data = emails[0]
            self.assertIn("from", email_data)
            self.assertIn("subject", email_data)
            self.assertIn("date", email_data)
            self.assertIn("body", email_data)
            self.assertIn("attachments", email_data)

    # Optional: if you later add send_email method
    # def test_send_email(self):
    #     """Send a test email via Zoho SMTP"""
    #     to_address = self.client.email_address
    #     subject = "Integration Test Email"
    #     body = "This is a test email sent by ZohoMailClient."
    #     result = self.client.send_email(to_address, subject, body)
    #     self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
