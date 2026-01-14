Name:Atharva Ravindra Kale

1.## Architecture Diagram
![Architecture Diagram](Architecture.png)

Diagram:(Textual Architecture)
+———————+
|        User         |
|   (Gmail Account)   |
+–––––+–––––+
|
| OAuth 2.0 Authentication
|
+–––––v–––––+
|     Google OAuth    |
|   Consent Screen    |
+–––––+–––––+
|
| Access Token (token.json)
|
+–––––v–––––+
|    Python Script    |
|   (src/main.py)     |
+–––––+–––––+
|
| Fetch unread emails
|
+–––––v–––––+
|      Gmail API      |
|  (Inbox, Unread)    |
+–––––+–––––+
|
| Email ID, headers, body
|
+–––––v–––––+
|    Email Parser     |
| (email_parser.py)  |
+–––––+–––––+
|
| From, Subject, Date, Content
|
+–––––v–––––+
|   Duplicate Check   |
|    (state.json)     |
+–––––+–––––+
|
| New emails only
|
+–––––v–––––+
| Google Sheets API   |
|   (Append Rows)     |
+–––––+–––––+
|
| Stored as rows
|
+–––––v–––––+
|    Google Sheet     |
+———————+



2.Step-by-Step Setup Instructions

Prerequisites
	•	Python 3.9+
	•	Google account
	•	Google Cloud Project
	•	Gmail & Google Sheets APIs enabled

Step 1: Clone Repository
git clone <repo-url>
cd gmail-to-sheets

Step 2: Create Virtual Environment
python3 -m venv venv
source venv/bin/activate

Step 3: Install Dependencies
pip install -r requirements.txt

Step 4: Configure Google Cloud
	1.	Create a Google Cloud project
	2.	Enable:
	•	Gmail API
	•	Google Sheets API
	3.	Create OAuth 2.0 Client (Desktop App)
	4.	Download credentials.json
	5.	Place it inside:
        credentials/credentials.json

Step 5: Configure Google Sheet
	•	Create a Google Sheet
	•	Add headers in row 1:
        From | Subject | Date | Content
    •	Copy the Spreadsheet ID
	•	Update config.py

Step 6: Run the Script
        python -m src.main
        
        On first run:
	•	Browser opens for OAuth login
	•	Token is saved locally
	•	Emails are processed

3.Design Explanations

OAuth Flow Used
•	Uses OAuth 2.0 Installed App Flow
•	User grants permission via browser
•	Access & refresh tokens are stored in token.json
•	Tokens are reused on subsequent runs without re-login
•	No service accounts are used

⸻

Duplicate Prevention Logic
	•	Each Gmail email has a unique message ID
	•	Before processing, the script checks if the ID already exists
	•	If found, the email is skipped
        code logic:
        if msg["id"] in processed:
             continue

State Persistence Method
	•	Processed message IDs are stored in state.json
	•	This file is read at startup and updated after execution
	•	Ensures idempotent execution

    Example:
    [
      "18c9f8e9d9a3b7a1",
      "18c9f8e9d9a3b7a2"
    ]

4. Challenges Faced & Solutions

Challenge: Duplicate emails being processed on re-run

Problem:
Re-running the script could reprocess the same emails.

Solution:
Used Gmail message IDs and persisted them in state.json.
This ensures already-processed emails are skipped permanently.

⸻

Challenge: HTML-only email content

Problem:
Some emails do not contain plain text.

Solution:
Implemented HTML → plain-text fallback using BeautifulSoup.

⸻

Challenge: OAuth access blocked error

Problem:
Google blocked access for unregistered users.

Solution:
Added the Gmail account as a Test User in OAuth consent screen.

⸻

5. Limitations of the Solution
	•	Designed for single-user execution
	•	Requires the system to be powered on for cron scheduling
	•	Google OAuth app is in testing mode
	•	Sheet grows indefinitely without archival
	•	Not suitable for public multi-user usage without verification
