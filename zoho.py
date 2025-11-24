import imaplib, os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")
HOST = os.getenv("EMAIL_HOST")
PORT = int(os.getenv("EMAIL_PORT"))

try:
    mail = imaplib.IMAP4_SSL(HOST, PORT)
    mail.login(EMAIL, PASSWORD)
    mail.select("Inbox")
    status, messages = mail.search(None, "ALL")
    print("✅ Connected. Found", len(messages[0].split()), "emails.")
except Exception as e:
    print("❌ Failed:", e)
