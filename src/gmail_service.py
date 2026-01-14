
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from config import GMAIL_SCOPES

TOKEN_FILE = "token.json"
CREDENTIALS_FILE = "credentials/credentials.json"


def get_gmail_service():
    creds = None

    # Load existing token
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(
            TOKEN_FILE, GMAIL_SCOPES
        )

    # If token is invalid or missing, re-authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, GMAIL_SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save token
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def fetch_unread_emails(service):
    """
    Fetch unread emails from Inbox
    """
    response = service.users().messages().list(
        userId="me",
        q="is:unread in:inbox"
    ).execute()

    return response.get("messages", [])
