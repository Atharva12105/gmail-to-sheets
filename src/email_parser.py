import base64
from bs4 import BeautifulSoup
from email.utils import parsedate_to_datetime

def parse_email(service, msg_id):
    msg = service.users().messages().get(
        userId="me", id=msg_id, format="full"
    ).execute()

    headers = msg["payload"]["headers"]
    data = {"From": "", "Subject": "", "Date": "", "Content": ""}

    for h in headers:
        if h["name"] in data:
            data[h["name"]] = h["value"]

    parts = msg["payload"].get("parts", [])

    # 1️⃣ Try to extract text/plain first
    for part in parts:
        if part["mimeType"] == "text/plain" and "data" in part["body"]:
            body = base64.urlsafe_b64decode(
                part["body"]["data"]
            ).decode(errors="ignore")
            data["Content"] = body
            return data   # ✅ stop once plain text is found

    # 2️⃣ Fallback to text/html if plain text not found
    for part in parts:
        if part["mimeType"] == "text/html" and "data" in part["body"]:
            html = base64.urlsafe_b64decode(
                part["body"]["data"]
            ).decode(errors="ignore")
            soup = BeautifulSoup(html, "html.parser")
            data["Content"] = soup.get_text()
            return data

    return data
