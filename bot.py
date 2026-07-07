import os
import time
import subprocess
import requests
from dotenv import load_dotenv

# Load credentials from your local secret file
load_dotenv()

GITHUB_REPO = "Readeasy30/my-openclaw-bot"
TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"token {TOKEN}" if TOKEN else "",
    "Accept": "application/vnd.github.v3+json"
}

def check_maintenance_jobs():
    """Polls a specific dispatch file in the repo for system commands."""
    url = f"https://github.com{GITHUB_REPO}/contents/maintenance_jobs.txt"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        # File exists, decode the system task instructions here
        print("Found active maintenance job dispatch.")
        # Logic to parse and safely execute scripts locally goes here
    elif response.status_code == 404:
        print("No pending maintenance jobs found in repository.")

def main():
    print("my-openclaw-bot local listener initialized...")
    while True:
        try:
            check_maintenance_jobs()
            time.sleep(60)  # Check for new repo commands every 60 seconds
        except KeyboardInterrupt:
            print("Shutting down bot listener.")
            break

if __name__ == "__main__":
    main()
