import subprocess
import sys
import os
import glob

def run_step(description, command):
    """Executes a pipeline step and handles terminal output."""
    print(f"\n--- 🚀 {description} ---")
    try:
        # Runs the command and pipes the output directly to your terminal
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}: {e}")
        return False

def main():
    print("🛡️  STARTING GUARDIAN-AUTH ARCHITECT PIPELINE")
    print("==============================================")

    # --- PHASE 1: SECURITY AUDITING ---
    if not run_step("Phase 1: Security Auditing", ["python3", "src/security_auditor.py"]):
        print("🚨 Critical failure in Security Auditor. Aborting.")
        sys.exit(1)

    # --- 🚦 GATE 1: ARCHITECT REVIEW ---
    print("\n" + "!"*45)
    user_input = input("🛑 SECURITY AUDIT COMPLETE. Review findings above.\nDo you approve these requirements? (y/n): ")
    if user_input.lower() != 'y':
        print("❌ Pipeline terminated by Architect. No tickets created.")
        sys.exit(0)

    # --- PHASE 2: JIRA SYNCHRONIZATION ---
    # CHANGED: Now runs the actual Analyst Agent instead of just the test script
    if not run_step("Phase 2: Jira Synchronization", ["python3", "src/analyst_agent.py"]):
        print("⚠️  Warning: Jira sync failed. Check your .env and Jira project key.")

    # --- 🚦 GATE 2: DEV AUTHORIZATION ---
    user_input = input("\n🚀 Ready to authorize AI Code Generation? (y/n): ")
    if user_input.lower() != 'y':
        print("❌ Pipeline terminated by Architect. No code modified.")
        sys.exit(0)

    # --- PHASE 3: AUTOMATED CODE GENERATION ---
    if not run_step("Phase 3: Automated Code Generation", ["python3", "src/developer_agent.py"]):
        print("🚨 Code generation failed. Check LLM connectivity.")
        sys.exit(1)

    # --- PHASE 4: LOGIC VERIFICATION ---
    # CHANGED: Dynamic discovery of test files instead of hardcoded 'test_SEC_67.py'
    test_files = glob.glob("src/generated_code/test_*.py")
    
    if not test_files:
        print("🚨 Error: No test files were found in src/generated_code/. Phase 3 likely failed to save files.")
        sys.exit(1)

    print(f"🧪 Running verification on {len(test_files)} generated test(s)...")
    
    # We run pytest on the entire directory to catch all generated tests
    if not run_step("Phase 4: Logic Verification", ["python3", "-m", "pytest", "src/generated_code/"]):
        print("🚨 Logic Verification FAILED. Do not deploy this code!")
        sys.exit(1)

    print("\n" + "="*46)
    print("✅ MISSION ACCOMPLISHED: All agents successfully orchestrated.")
    print("🛡️  System Status: AUDITED | CODED | VERIFIED")
    print("="*46)

if __name__ == "__main__":
    main()