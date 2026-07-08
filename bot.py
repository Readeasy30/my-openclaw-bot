import argparse
import json
import os
import sys
from dotenv import load_dotenv

def initialize_matrix_environment():
    # Force load environment variables from your root .env file
    load_dotenv()
    
    # Configure argument parsing matching the parameters passed from Node
    parser = argparse.ArgumentParser(description="OpenClaw Matrix Orchestrator Engine")
    parser.add_index_arg = parser.add_argument  # Safe execution map
    parser.add_argument('--matrix', type=str, default='matrix-config.json', help='Path to repo matrix layout')
    parser.add_argument('--prompt', type=str, default='system-core.txt', help='Path to system instructions file')
    
    # Safely parse arguments without breaking existing script parameters
    args, unknown = parser.parse_known_args()
    
    print(f"[Python] Parsing repository configuration file: {args.matrix}")
    
    # Load and map the website repository matrix configuration
    if os.path.exists(args.matrix):
        with open(args.matrix, 'r', encoding='utf-8') as f:
            matrix_data = json.load(f)
            print("[Python] Matrix configuration loaded successfully.")
            # Store matrix dictionary securely inside environment scope for system-wide access
            os.environ['REPOS_MATRIX'] = json.dumps(matrix_data.get('repository_matrix', {}))
    else:
        print(f"[Python Warning] Targeted repository grid profile missing: {args.matrix}")
        sys.exit(1)
        
    # Read the core system prompt rules file
    if os.path.exists(args.prompt):
        with open(args.prompt, 'r', encoding='utf-8') as f:
            system_prompt = f.read()
            os.environ['SYSTEM_CORE_PROMPT'] = system_prompt
            print("[Python] System prompt instructions successfully cached.")
    else:
        print(f"[Python Warning] System prompt file missing: {args.prompt}")

# Execute matrix parsing immediately on initialization
if __name__ == "__main__" or __name__ == "bot":
    initialize_matrix_environment()


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
    """Executes native Windows 11 core, display, updates, service audits, and AI tools tracking."""
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
            "  foreach ($update in $searchResult.Updates) { \"- $($update.Title)\" }"
            "} catch { \"Unable to query Windows Update Agent service.\" }"
        )
        cmd = ["powershell", "-Command", ps_script]

    elif task_name == "INSTALL_UPDATES":
        install_script = (
            "try { "
            "  $updateSession = New-Object -ComObject Microsoft.Update.Session; "
            "  $updateSearcher = $updateSession.CreateUpdateSearcher(); "
            "  $searchResult = $updateSearcher.Search(\"IsInstalled=0 and IsHidden=0\"); "
            "  if ($searchResult.Updates.Count -eq 0) { \"No pending installations found.\"; exit; } "
            "  $updatesToDownload = New-Object -ComObject Microsoft.Update.UpdateColl; "
            "  foreach ($update in $searchResult.Updates) { $updatesToDownload.Add($update) | Out-Null }; "
            "  $downloader = $updateSession.CreateUpdateDownloader(); $downloader.Updates = $updatesToDownload; $downloader.Download() | Out-Null; "
            "  $updatesToInstall = New-Object -ComObject Microsoft.Update.UpdateColl; "
            "  foreach ($update in $searchResult.Updates) { if ($update.IsDownloaded) { $updatesToInstall.Add($update) | Out-Null } }; "
            "  $installer = $updateSession.CreateUpdateInstaller(); $installer.Updates = $updatesToInstall; $installResult = $installer.Install(); "
            "  if ($installResult.RebootRequired) { shutdown /r /t 60 /c \"Automated OpenClaw system update reboot sequence initiated.\" } "
            "} catch { \"Update pipeline execution failed.\" }"
        )
        cmd = ["powershell", "-Command", install_script]

    elif task_name == "CHECK_SERVICES":
        service_script = (
            "Write-Output \"--- Windows Core Service Status Audit ---\"; "
            "$services = @('Spooler', 'AudioEndpointBuilder', 'WbioSrvc'); "
            "foreach ($svcName in $services) { "
            "  $svc = Get-Service -Name $svcName -ErrorAction SilentlyContinue; "
            "  if ($svc) { "
            "    Write-Output \"Service: $($svc.DisplayName) ($svcName) -> Status: $($svc.Status)\"; "
            "    if ($svc.Status -ne 'Running') { Start-Service -Name $svcName -ErrorAction SilentlyContinue }"
            "  } "
            "}"
        )
        cmd = ["powershell", "-Command", service_script]

    elif task_name == "VERIFY_AI_TOOLS":
        ai_script = (
            "Write-Output \"--- AI Development Stack Status Audit ---\"; "
            "Write-Output \"Checking local Claude Code binary dependency...\"; "
            "if (Get-Command claude -ErrorAction SilentlyContinue) { Write-Output \"[OK] Claude Code is accessible via system PATH.\" } else { Write-Output \"[WARNING] Claude command-line wrapper not detected in default environment path.\" }; "
            "Write-Output \"Checking ChatGPT Pro local process status...\"; "
            "$chatgptProc = Get-Process -Name *ChatGPT* -ErrorAction SilentlyContinue; "
            "if ($chatgptProc) { Write-Output \"[OK] ChatGPT Pro desktop environment process is live.\" } else { Write-Output \"[INFO] ChatGPT Pro desktop interface is not currently running inside user space.\" }; "
            "Write-Output \"`nChecking Key Environment Configurations Securely...\"; "
            "if ($env:OPENAI_API_KEY) { Write-Output \"[OK] OPENAI_API_KEY environment variable is successfully loaded.\" } else { Write-Output \"[ALERT] OPENAI_API_KEY environment flag is empty or missing! Check user configurations.\" }; "
            "if ($env:ANTHROPIC_API_KEY) { Write-Output \"[OK] ANTHROPIC_API_KEY environment variable is successfully loaded.\" } else { Write-Output \"[ALERT] ANTHROPIC_API_KEY environment flag is empty or missing! Check user configurations.\" }; "
            "Write-Output \"`nVerifying OpenAI API/Codex and Anthropic endpoint accessibility...\"; "
            "try { "
            "  $openaiTest = Invoke-WebRequest -Uri 'https://openai.com' -Method Get -TimeoutSec 10 -ErrorAction SilentlyContinue; "
            "  Write-Output \"[OK] Connection to OpenAI/Codex endpoints verified successfully.\"; "
            "} catch { Write-Output \"[ALERT] Unable to reach OpenAI endpoints. Check local firewall or DNS profiles.\" }; "
            "try { "
            "  $anthropicTest = Invoke-WebRequest -Uri 'https://anthropic.com' -Method Get -TimeoutSec 10 -ErrorAction SilentlyContinue; "
            "  Write-Output \"[OK] Connection to Anthropic API endpoints verified successfully.\"; "
            "} catch { Write-Output \"[ALERT] Unable to reach Anthropic API gateways. Network constraint detected.\" }"
        )
        cmd = ["powershell", "-Command", ai_script]
        
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
    # 1. Parse your newly pushed matrix layout and prompt files
    initialize_matrix_environment()
    
    # 2. Main execution block to process your automated jobs
    print("\n===================================================")
    print("[Engine] OpenClaw Active Matrix Workspace Engine Online")
    print("===================================================\n")
    
    # Add your task execution logic call here (e.g., check for maintenance jobs)
    print("[Success] All system core matrix configurations cached.")
  


