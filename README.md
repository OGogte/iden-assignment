# Notion Team Members Automation - Integration Engineer Job Assessment

## Objective
This project automates the process of fetching and parsing the list of members in a Notion team using Python and Playwright. The script logs into Notion, captures the team members' data via API calls, and outputs the following information for each member into a JSON file:
- Name
- Email
- Role
- Is Admin (boolean)
- Created At (formatted date)

## Prerequisites
Before running the script, ensure you meet the following requirements:

**Notion Account**: Create a new Notion account if you don't already have one.

**Important**: Ensure the account you use has access to team member information and API interaction capabilities.

## Task Requirements Fulfilled
- Automates login to Notion and navigation to the team members page.
- Identifies the Notion API endpoints (`getVisibleUsers` and `syncRecordValues`) to fetch member data.
- Parses the fetched data and exports a JSON file with required fields.

## Features
- **Automatic Login**: Script logs into Notion using Playwright and a custom `login` function. It can also store session cookies to avoid re-login.
- **API Data Capture**: Fetches and processes team member data through Notion's API.

- **Data Parsing**: Extracts relevant data (Name, Email, Role, Created At) and formats it into a JSON file.
- **Error Handling**: Includes proper error handling for network timeouts, API issues, and invalid data.

## Project Structure

```bash
.
├── README.md                # Project documentation
├── invite_teammates.py      # Automation script to invite teammates
├── notion_automation.py     # Main automation script
├── login.py                 # Login functionality
├── requirements.txt         # Required libraries
└── final_user_data.json     # Sample output JSON
```

## Run Locally

Clone the project

```bash
  git clone https://github.com/OGogte/iden-assignment.git
```

Go to the project directory

```bash
  cd iden-assignment
```

Install dependencies

```bash
  pip install -r requirements.txt
```
The key dependencies are:

- playwright: For browser automation.
- faker: To generate fake data for team members.
- datetime: For timestamp conversion.
- json: For reading/writing JSON data.

```bash
  playwright install
```
Invite fake teammates
```bash
 python invite_teammates.py
```

Fetch data
```bash
python notion_automation.py
```
View the Output After the script runs successfully, a JSON file (final_user_data.json) will be created containing details of all team members.

**Please Note** - isAdmin could not be added because admin feature is paid and I could not verify how isAdmin being sent in the api so have excluded that. 