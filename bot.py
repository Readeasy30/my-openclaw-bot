import os
import time
import base64
import subprocess
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_REPO = "Readeasy30/my-openclaw-bot"
TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"token {TOKEN}" if TOKEN else "",
    "Accept": "application/vnd.github.v3+json"
}

def clear_job_file(sha):
    """Clears the maintenance file on GitHub after the task is executed."""
    url = f"https://github.com{GITHUB_REPO}/contents/maintenance_jobs.txt"
    payload = {
        "message": "Maintenance task completed by bot",
        "content": base64.b64encode(b"IDLE").decode("utf-8"),
        "sha": sha
    }
    requests.put(url, headers=headers, json=payload)

def execute_windows_task(task_name):
    """Executes safe, native Windows 11 maintenance utilities."""
    print(f"Executing Windows 11 task: {task_name}")
    
    if task_name == "DISK_CHECK":
        # Checks primary drive health status using WMIC
        cmd = ["powershell", "-Command", "Get-Volume"]
    elif task_name == "CLEAR_TEMP":
        # Safely deletes temporary user files
        cmd = ["powershell", "-Command", "Remove-Item -Path $env:TEMP\\* -Recurse -Force -ErrorAction SilentlyContinue"]
    else:
        print("Unknown or unsupported command.")
        return

    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    print("--- Execution Output ---")
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)

def check_maintenance_jobs():
    """Polls your GitHub repository for active Windows instructions."""
    url = f"https://github.com{GITHUB_REPO}/contents/maintenance_jobs.txt"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        content = base64.b64decode(data["content"]).decode("utf-8").strip()
        sha = data["sha"]
        
        if content and content != "IDLE":
            execute_windows_task(content)
            clear_job_file(sha)
    elif response.status_code == 404:
        print("Missing maintenance_jobs.txt file in the repository.")

def main():
    print("my-openclaw-bot actively listening for Windows 11 commands...")
    while True:
        try:
            check_maintenance_jobs()
            time.sleep(30)  # Scan repository every 30 seconds
        except KeyboardInterrupt:
            print("Shutting down bot safely.")
            break

if __name__ == "__main__":
    main()


