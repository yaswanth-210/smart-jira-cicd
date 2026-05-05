import os
import requests
from dotenv import load_dotenv

load_dotenv()

JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

def get_issues():
    url = f"{JIRA_URL}/rest/api/3/search/jql"

    headers = {
        "Accept": "application/json"
    }

    params = {
        "jql": "project = SC ORDER BY created DESC",
        "maxResults": 10
    }

    auth = (JIRA_EMAIL, JIRA_API_TOKEN)

    response = requests.get(url, headers=headers, params=params, auth=auth)
    return response.json()