from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from config import SHEETS_SCOPES, SPREADSHEET_ID, SHEET_NAME
import json, os

def get_sheets_service():
    flow = InstalledAppFlow.from_client_secrets_file(
        "credentials/credentials.json", SHEETS_SCOPES
    )
    creds = flow.run_local_server(port=0)
    return build("sheets", "v4", credentials=creds)

def append_rows(service, rows):
    body = {"values": rows}
    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=SHEET_NAME,
        valueInputOption="RAW",
        body=body
    ).execute()
