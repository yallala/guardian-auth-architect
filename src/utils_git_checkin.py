import subprocess
import datetime

def run_git_workflow():
    print("\n📦 Git Utility: Committing Full Pipeline State...")
    try:
        # 1. Add everything (Infrastructure + Generated Code)
        subprocess.run(["git", "add", "."], check=True)
        
        # 2. Check for changes
        git_status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if not git_status.stdout.strip():
            print("✨ No changes detected. Environment is clean.")
            return

        # 3. Commit
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_msg = f"🛡️ Pipeline Sync: Verified Build [{timestamp}]"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        
        # 4. Push
        print("🚀 Pushing to GitHub...")
        subprocess.run(["git", "push"], check=True)
        print("✨ Deployment Successful.")
        
    except Exception as e:
        print(f"❌ Git Workflow Failed: {e}")

if __name__ == "__main__":
    run_git_workflow()