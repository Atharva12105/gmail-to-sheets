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



2️⃣ Step-by-Step Setup Instructions

Prerequisites
	•	Python 3.9 or higher
	•	Google account
	•	Google Cloud Project
	•	Gmail API enabled
	•	Google Sheets API enabled
	
Step 1: Clone the Repository
git clone <your-repository-url>
cd gmail-to-sheets

Step 2: Create Virtual Environment
python3 -m venv venv
source venv/bin/activate

Step 3: Install Dependencies
pip install -r requirements.txt

Step 4: Configure Google Cloud
	1.	Create a Google Cloud project.
	2.	Enable the following APIs:
	•	Gmail API
	•	Google Sheets API
	3.	Create an OAuth 2.0 Client ID.
	•	Application type: Desktop App
	4.	Download the credentials.json file.
	5.	Place it inside:credentials/credentials.json

Step 5: Configure Google Sheet
	•	Create a Google Sheet.
	•	Add the following headers in the first row:
	•	From
	•	Subject
	•	Date
	•	Content
	•	Copy the Spreadsheet ID from the URL.
	•	Update config.py with:
	•	Spreadsheet ID
	•	Sheet name

Step 6: Run the Script:- python -m src.main
      	•	Browser opens for OAuth consent on first run
	    •	Token is stored locally
	    •	Emails are fetched and logged

3. Design Explanations

🔐 OAuth Flow Used
	•	Uses OAuth 2.0 Installed App Flow
	•	User grants permission via browser on first run
	•	Access and refresh tokens are stored locally in token.json
	•	Tokens are reused on subsequent executions without re-login
	•	No service accounts are used

⸻

Duplicate Prevention Logic
	•	Each Gmail email has a unique message ID
	•	Before processing, the script checks if the ID already exists
	•	If found, the email is skipped
        code logic:
        if msg["id"] in processed:
             continue

🗂️ State Persistence Method
	•	Processed Gmail message IDs are stored in state.json
	•	This file is read at script startup
	•	It is updated after each successful execution
	•	Ensures idempotent execution, meaning the script can be safely run multiple times
	
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

5.Limitations of the Solution
	•	Designed for single-user execution
	•	Requires the system to be powered on and awake for cron-based scheduling
	•	Google OAuth application remains in testing mode
	•	Google Sheet grows indefinitely without automatic archival
	•	Not suitable for public multi-user usage without OAuth verification
