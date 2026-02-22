import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth

# Load your 'Vault' variables
load_dotenv()

# Build the connection URL
url = f"{os.getenv('JIRA_SITE_URL')}/rest/api/3/project/{os.getenv('JIRA_PROJECT_KEY')}"
auth = HTTPBasicAuth(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN"))

# Send a request to Jira
response = requests.request("GET", url, auth=auth)

if response.status_code == 200:
    print(f"✅ Success! Connected to project: {response.json()['name']}")
else:
    print(f"❌ Failed! Error code: {response.status_code}")
    print("Check your .env file details.")