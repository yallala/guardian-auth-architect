import os
from dotenv import load_dotenv
from jira import JIRA

# 1. Setup
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base_dir, '.env'))

def cleanup_backlog():
    jira = JIRA(
        server=os.getenv("JIRA_SERVER"),
        basic_auth=(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN"))
    )
    
    project_key = os.getenv("JIRA_PROJECT_KEY")
    
    # 2. Search for all stories in your project
    print(f"🔍 Searching for tickets in project {project_key}...")
    issues = jira.search_issues(f'project={project_key}')
    
    if not issues:
        print("✅ Backlog is already empty.")
        return

    # 3. Delete them
    print(f"🗑️ Found {len(issues)} tickets. Starting deletion...")
    for issue in issues:
        print(f"Deleting {issue.key}...")
        issue.delete()
    
    print("✨ Backlog is now clean! You have a fresh start.")

if __name__ == "__main__":
    cleanup_backlog()