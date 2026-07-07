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

def log_output_to_github(output_text):
    """Pushes execution output logs directly into maintenance_log.txt."""
    url = f"https://github.com{GITHUB_REPO}/contents/maintenance_log.txt"
    response = requests.get(url, headers=headers)
    sha = response.json().get("sha") if response.status_code == 200 else None
    
    payload = {
        "message": "Update execution logs from Windows 11 host",
        "content": base64.b64encode(output_text.encode("utf-8")).decode("utf-8"),
    }
    if sha:
        payload["sha"] = sha
        
    requests.put(url, headers=headers, json=payload)

def clear_job_file(sha):
    """Clears the maintenance file on GitHub after the task is executed."""
    url = f"https://github.com{GITHUB_REPO}/contents/maintenance_jobs.txt"
    payload = {
        "message": "Task processed",
        "content": base64.b64encode(b"IDLE").decode("utf-8"),
        "sha": sha
    }
    requests.put(url, headers=headers, json=payload)

def execute_windows_task(task_name):
    """Executes native Windows 11 core, display, telemetry, and update status tasks."""
    print(f"Executing: {task_name}")
    
    if task_name == "DISK_CHECK":
        cmd = ["powershell", "-Command", "Get-Volume | Out-String"]
    elif task_name == "CLEAR_TEMP":
        cmd = ["powershell", "-Command", "Remove-Item -Path $env:TEMP\\* -Recurse -Force -ErrorAction SilentlyContinue; Echo 'Temp cleared'"]
    elif task_name == "LIST_DISPLAYS":
        cmd = ["powershell", "-Command", "Get-CimInstance -Namespace root\\wmi -ClassName WmiMonitorBasicDisplayParams | Select-Object InstanceName, Active | Out-String"]
    elif task_name == "RESET_DISPLAYS":
        cmd = ["powershell", "-Command", "Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; public class Disp { [DllImport(\"user32.dll\")] public static extern bool SetProcessDPIAware(); }'; [Disp]::SetProcessDPIAware(); Echo 'Subsystem reset'"]
    elif task_name == "ARRANGE_DISPLAYS":
        cmd = ["powershell", "-Command", "DisplaySwitch.exe /extend; Echo 'Displays set to extend'"]
        
    elif task_name == "SYSTEM_ALERTS":
        # Fetches CPU load, Total free RAM, storage health margins, and critical Windows Update gaps simultaneously
        ps_script = (
            "$cpu = (Get-CimInstance Win32_Processor).LoadPercentage; "
            "$os = Get-CimInstance Win32_OperatingSystem; "
            "$freeRam = [Math]::Round($os.FreePhysicalMemory / 1024 / 1024, 2); "
            "$totalRam = [Math]::Round($os.TotalVisibleMemorySize / 1024 / 1024, 2); "
            "Write-Output \"--- Hardware Metrics Audit ---\"; "
            "Write-Output \"Current CPU Load: $cpu%\"; "
            "Write-Output \"Available RAM memory: $freeRam GB / $totalRam GB\"; "
            "if ($cpu -gt 85) { Write-Output \"ALERT: High CPU threshold exceeded!\" }; "
            "if (($freeRam / $totalRam) -lt 0.15) { Write-Output \"ALERT: System Memory reserves are low!\" }; "
            "Write-Output \"`n--- Windows Update Status Audit ---\"; "
            "try { "
            "  $updateSession = New-Object -ComObject Microsoft.Update.Session; "
            "  $updateSearcher = $updateSession.CreateUpdateSearcher(); "
            "  $searchResult = $updateSearcher.Search(\"IsInstalled=0 and IsHidden=0\"); "
            "  Write-Output \"Pending Updates Count: $($searchResult.Updates.Count)\"; "
            "  foreach ($update in $searchResult.Updates) { "
            "    Write-Output \"- $($update.Title)\" "
            "  }"
            "} catch { "
            "  Write-Output \"Unable to query Windows Update Agent service.\""
            "}"
        )
        cmd = ["powershell", "-Command", ps_script]
    else:
        return "Unsupported or unknown command."

    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    full_log = f"=== Log Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')} ===\n"
    full_log += f"STDOUT:\n{result.stdout}\n"
    if result.stderr:
        full_log += f"STDERR:\n{result.stderr}\n"
        
    return full_log

def check_maintenance_jobs():
    """Polls your GitHub repository for active Windows instructions."""
    url = f"https://github.com{GITHUB_REPO}/contents/maintenance_jobs.txt"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        content = base64.b64decode(data["content"]).decode("utf-8").strip()
        sha = data["sha"]
        
        if content and content != "IDLE":
            log_data = execute_windows_task(content)
            log_output_to_github(log_data)
            clear_job_file(sha)

def main():
    print("my-openclaw-bot system listener online...")
    while True:
        try:
            check_maintenance_jobs()
            time.sleep(30)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
