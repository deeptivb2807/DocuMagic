import os
import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

class ZohoMailClient:
    def __init__(self):
        # Load settings from .env
        self.imap_host = os.getenv("EMAIL_HOST", "imap.zoho.com")
        self.imap_port = int(os.getenv("EMAIL_PORT", 993))
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.zoho.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 465))
        self.email_address = os.getenv("EMAIL_ADDRESS")
        self.email_password = os.getenv("EMAIL_PASSWORD")

    def fetch_emails(self, limit=5):
        """Fetch recent emails from Zoho Mail inbox, including attachments"""
        try:
            mail = imaplib.IMAP4_SSL(self.imap_host, self.imap_port)
            mail.login(self.email_address, self.email_password)

            # List folders to detect the correct inbox name
            status, folders = mail.list()
            inbox_name = None
            for f in folders:
                f_decoded = f.decode()
                if "INBOX" in f_decoded.upper():
                    inbox_name = "INBOX"
                    break

            if not inbox_name:
                inbox_name = "INBOX"  # fallback

            mail.select(inbox_name)

            status, messages = mail.search(None, "ALL")
            email_ids = messages[0].split()

            results = []
            for eid in email_ids[-limit:]:
                status, msg_data = mail.fetch(eid, "(RFC822)")
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)

                # Extract plain text body if available
                body = None
                attachments = []
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))

                        # Plain text body
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            body = part.get_payload(decode=True).decode(errors="ignore")

                        # Attachments
                        if "attachment" in content_disposition:
                            filename = part.get_filename()
                            if filename:
                                file_data = part.get_payload(decode=True)

                                # ✅ Save file to disk
                                os.makedirs("uploads", exist_ok=True)
                                file_path = os.path.join("uploads", filename)
                                with open(file_path, "wb") as f:
                                    f.write(file_data)

                                attachments.append({
                                    "filename": filename,
                                    "size": len(file_data) if file_data else 0,
                                    "path": file_path
                                })
                else:
                    body = msg.get_payload(decode=True).decode(errors="ignore")

                results.append({
                    "from": msg.get("From"),
                    "subject": msg.get("Subject"),
                    "date": msg.get("Date"),
                    "body": body,
                    "attachments": attachments
                })

            mail.logout()
            return results

        except Exception as e:
            print("Zoho Mail fetch failed:", e)
            return []

    def send_email(self, to_address, subject, body):
        """Send an email via Zoho SMTP"""
        try:
            msg = MIMEText(body)
            msg["From"] = self.email_address
            msg["To"] = to_address
            msg["Subject"] = subject

            with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port) as server:
                server.login(self.email_address, self.email_password)
                server.sendmail(self.email_address, [to_address], msg.as_string())

            print("Email sent successfully to", to_address)
            return True

        except Exception as e:
            print("Zoho Mail send failed:", e)
            return False
