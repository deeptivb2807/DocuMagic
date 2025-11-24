import os
import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.models.document import Document  # adjust path if needed

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

    def fetch_emails(self, limit=5, db: Session = None, owner_id: int = None):
        """Fetch recent emails from Zoho Mail inbox, store only filename + file_type in DB"""
        try:
            mail = imaplib.IMAP4_SSL(self.imap_host, self.imap_port)
            mail.login(self.email_address, self.email_password)

            mail.select("INBOX")
            status, messages = mail.search(None, "ALL")
            email_ids = messages[0].split()

            results = []
            for eid in email_ids[-limit:]:
                status, msg_data = mail.fetch(eid, "(RFC822)")
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)

                body = None
                attachments = []
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition") or "")

                        # Extract plain text body
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            try:
                                body = part.get_payload(decode=True).decode(errors="ignore")
                            except Exception:
                                body = None

                        # Extract attachments
                        if "attachment" in content_disposition:
                            filename = part.get_filename()
                            if filename:
                                # derive file type from extension
                                file_type = os.path.splitext(filename)[1].replace(".", "").lower()

                                attachments.append({
                                    "filename": filename,
                                    "file_type": file_type
                                })

                                # Store directly in DB (only filename + file_type)
                                if db and owner_id:
                                    try:
                                        doc = Document(
                                            filename=filename,
                                            file_type=file_type,
                                            owner_id=owner_id
                                        )
                                        db.add(doc)
                                        db.commit()
                                        db.refresh(doc)
                                        print(f"Inserted document {doc.id}: {filename} ({file_type})")
                                    except Exception as e:
                                        db.rollback()
                                        print(f"DB insert failed for {filename}: {e}")

                else:
                    try:
                        body = msg.get_payload(decode=True).decode(errors="ignore")
                    except Exception:
                        body = None

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
