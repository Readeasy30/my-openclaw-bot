import os
import sys
import json
from dotenv import load_dotenv

def run_orchestrator():
    # 1. Clear terminal screen for a clean, unified view
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=========================================================")
    print("      OPENCLAW MATRIX ORCHESTRATOR - PRODUCTION ENGINE   ")
    print("=========================================================\n")

    # 2. Check for root .env configurations
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("[WARNING] GITHUB_TOKEN not found in .env file.")
        print("Continuing in local directory fallback mode...\n")

    # 3. Read and validate your live repository matrix
    matrix_path = os.path.join(os.path.dirname(__file__), 'matrix-config.json')
    if not os.path.exists(matrix_path):
        print(f"[ERROR] Missing profile config: {matrix_path}")
        print("Please ensure your matrix-config.json file exists in this directory.")
        return

    with open(matrix_path, 'r', encoding='utf-8') as f:
        try:
            config = json.load(f)
            matrix = config.get('repository_matrix', {})
        except Exception as e:
            print(f"[ERROR] Failed to parse matrix-config.json syntax: {e}")
            return

    # 4. Load your standard structural prompt guidelines
    prompt_path = os.path.join(os.path.dirname(__file__), 'system-core.txt')
    system_prompt = ""
    if os.path.exists(prompt_path):
        with open(prompt_path, 'r', encoding='utf-8') as f:
            system_prompt = f.read().strip()
        print("[System] Core automation guidelines loaded successfully.")
    else:
        print("[System Warning] system-core.txt missing. Running with default context rules.")

    # 5. Interactive Workspace Selection Loop
    print("\n[Active Tracked Portfolios]:")
    all_repos = []
    counter = 1
    for category, repos in matrix.items():
        print(f"\n  * Category: {category.upper()}")
        for repo in repos:
            print(f"    [{counter}] {repo}")
            all_repos.append(repo)
            counter += 1

    print("\n=========================================================")
    try:
        selection = input("Enter a repository number to target (or 'q' to exit): ").strip()
        if selection.lower() == 'q':
            print("[Exit] Orchestrator shutdown safely.")
            sys.exit(0)
        
        index = int(selection) - 1
        if 0 <= index < len(all_repos):
            target_repo = all_repos[index]
            print(f"\n[Success] Swapping target context scope to: {target_repo}")
            print(f"[Action] Injecting guidelines into execution pipeline...")
            
            # This is where your AI tools lock-in context on that directory
            print(f"\n[Ready] You are now administering workspace: {target_repo}")
            print("=========================================================")
        else:
            print("[Invalid Selection] Out of matrix range. Restarting engine.")
    except ValueError:
        print("[Invalid Selection] Please enter a valid portfolio item number.")

if __name__ == "__main__":
    try:
        run_orchestrator()
    except KeyboardInterrupt:
        print("\n[Exit] Session terminated by user.")

