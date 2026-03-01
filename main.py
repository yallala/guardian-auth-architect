import sys, os, time, importlib.util, subprocess
from dotenv import load_dotenv
from jira import JIRA

# Load environment
base_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(base_dir, '.env'))

# Helper for dynamic imports
def import_agent(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# Load agents
analyst = import_agent("analyst", "src/02_analyst_agent.py")
coder = import_agent("coder", "src/04_coder_agent.py")
qa = import_agent("qa", "src/05_qa_tester_agent.py")

def purge_jira_backlog():
    print("\n--- 🧨 Phase 0.2: Jira Backlog Purge ---")
    try:
        jira = JIRA(server=os.getenv("JIRA_SERVER"), basic_auth=(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN")))
        issues = jira.search_issues(f'project={os.getenv("JIRA_PROJECT_KEY")}', maxResults=100)
        for issue in issues: issue.delete()
        print("✅ Jira Reset Complete.")
    except Exception as e: print(f"⚠️ Jira Purge failed: {e}")

def main():
    print("🛡️  STARTING GUARDIAN-AUTH ARCHITECT PIPELINE")
    
    # Reset Environment
    subprocess.run(["python3", "src/utils_reset_build.py"])
    purge_jira_backlog()

    # Step 1: Audit
    subprocess.run(["python3", "src/01_auditor_agent.py"])

    # Gate 1: Human Approval
    if input("\n🛑 Approve audit findings? (y/n): ").lower() != 'y': sys.exit(0)

    # Step 2: Jira Sync
    ticket_keys = analyst.run_analyst_workflow() 
    if not ticket_keys: sys.exit(1)

    # Gate 2: Dev Authorization
    if input(f"\n🚀 {len(ticket_keys)} tickets synced. Authorize AI? (y/n): ").lower() != 'y': sys.exit(0)

    time.sleep(3) # Let Jira catch up

    # Steps 3 & 4: Build & Test
    for key in ticket_keys:
        print(f"⚙️  Processing {key}...")
        if coder.build_feature(key):
            qa.validate_feature(key)

    # Step 5: Verification
    print("\n--- 🚀 Phase 5: Logic Verification ---")
    result = subprocess.run(["python3", "-m", "pytest", "src/generated_code/"])

    if result.returncode == 0:
        print("\n✅ VERIFICATION PASSED. Pushing to Git...")
        subprocess.run(["python3", "src/utils_git_checkin.py"])
    else:
        print("\n🚨 VERIFICATION FAILED. Quality Gate Closed.")
        sys.exit(1)

if __name__ == "__main__":
    main()