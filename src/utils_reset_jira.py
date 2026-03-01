# Purpose: Acts as the "Cleanup Crew" to wipe the Jira board and local files for a fresh start.
# Relationship: This is a standalone tool used by the Architect to reset the environment before a new run.

import os
from dotenv import load_dotenv
from jira import JIRA

# 1. Setup
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base_dir, '.env'))

def cleanup_backlog():
    # Initialize connection
    jira = JIRA(
        server=os.getenv("JIRA_SERVER"),
        basic_auth=(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN"))
    )
    
    project_key = os.getenv("JIRA_PROJECT_KEY")
    
    print(f"🧨 Starting Nuclear Cleanup for project: {project_key}")
    print("-" * 45)

    total_deleted = 0
    
    # 2. Continuous Loop to handle Pagination (More than 50 tickets)
    while True:
        # Fetch a batch of up to 100 tickets
        issues = jira.search_issues(f'project="{project_key}"', maxResults=100)
        
        if not issues:
            break
            
        print(f"📦 Found batch of {len(issues)} tickets. Purging...")
        
        for issue in issues:
            try:
                # deleteSubtasks=True handles hidden children that block deletion
                issue.delete(deleteSubtasks=True)
                total_deleted += 1
                if total_deleted % 10 == 0:
                    print(f"🔥 Progress: {total_deleted} tickets removed...")
            except Exception as e:
                print(f"⚠️ Could not delete {issue.key}: {e}")

    if total_deleted == 0:
        print("✅ Backlog was already empty.")
    else:
        print(f"✨ SUCCESS: {total_deleted} tickets permanently removed.")
        print("🖥️  Note: Jira web UI may take a few seconds to refresh the index.")

if __name__ == "__main__":
    cleanup_backlog()