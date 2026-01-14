import json, os
import logging
from src.gmail_service import get_gmail_service, fetch_unread_emails
from src.sheets_service import get_sheets_service, append_rows
from src.email_parser import parse_email
from config import STATE_FILE


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

processed = set()
if os.path.exists(STATE_FILE):
    processed = set(json.load(open(STATE_FILE)))

gmail = get_gmail_service()
sheets = get_sheets_service()

rows = []
messages = fetch_unread_emails(gmail)



logging.info("Fetching unread emails from Gmail")

for msg in messages:
    if msg["id"] in processed:
        logging.info("Skipping already processed email")
        continue

    data = parse_email(gmail, msg["id"])
    subject = data["Subject"].lower()
    sender = data["From"].lower()

    # Exclude no-reply emails
    if "no-reply" in sender or "noreply" in sender:
        logging.info(f"Skipping no-reply email: {data['Subject']}")
        gmail.users().messages().modify(
            userId="me",
            id=msg["id"],
            body={"removeLabelIds": ["UNREAD"]}
        ).execute()
        processed.add(msg["id"])
        continue

    # Subject-based filter
    if "invoice" not in subject:
        logging.info(f"Skipping non-invoice email: {data['Subject']}")
        gmail.users().messages().modify(
            userId="me",
            id=msg["id"],
            body={"removeLabelIds": ["UNREAD"]}
        ).execute()
        processed.add(msg["id"])
        continue

    rows.append([
        data["From"],
        data["Subject"],
        data["Date"],
        data["Content"]
    ])

    logging.info(f"Processed email: {data['Subject']}")

    gmail.users().messages().modify(
        userId="me",
        id=msg["id"],
        body={"removeLabelIds": ["UNREAD"]}
    ).execute()

    processed.add(msg["id"])
    
logging.info(f"Total rows ready to append: {len(rows)}")

if rows:
    append_rows(sheets, rows)
    logging.info(f"Appended {len(rows)} rows to Google Sheets")
else:
    logging.info("No new emails to append")

json.dump(list(processed), open(STATE_FILE, "w"))



