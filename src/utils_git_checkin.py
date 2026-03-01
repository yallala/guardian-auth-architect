import subprocess
import datetime
import os

def run_git_workflow():
    print("\n📦 Git Utility: Committing Verified Code...")
    
    try:
        # 1. Stage the verified code folder
        subprocess.run(["git", "add", "src/generated_code/"], check=True)
        
        # 2. Check for changes (prevents empty commit errors)
        # Fixed: Corrected the variable name and subprocess call
        git_status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        
        if not git_status.stdout.strip():
            print("✨ No changes detected in generated_code. Skipping Git push.")
            return

        # 3. Commit with a timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_msg = f"🛡️ Verified AI Logic Check-in: {timestamp}"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        
        # 4. Push
        print("🚀 Pushing to GitHub...")
        subprocess.run(["git", "push"], check=True)
        print("✨ Deployment Successful.")
        
    except Exception as e:
        print(f"❌ Git Workflow Failed: {e}")

if __name__ == "__main__":
    run_git_workflow()