import subprocess
import sys

def run_step(description, command):
    """Executes a pipeline step and handles terminal output."""
    print(f"\n--- 🚀 {description} ---")
    try:
        # Runs the command and pipes the output directly to your terminal
        subprocess.run(command, check=True, shell=isinstance(command, str))
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
    # We allow the pipeline to continue even if Jira fails (Local-First mode)
    if not run_step("Phase 2: Jira Synchronization", ["python3", "test_jira.py"]):
        print("⚠️  Warning: Jira sync failed (404/Connection). Proceeding in Local Mode...")

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
    if not run_step("Phase 4: Logic Verification", ["python3", "-m", "pytest", "src/generated_code/test_SEC_67.py"]):
        print("🚨 Logic Verification FAILED. Do not deploy this code!")
        sys.exit(1)

    print("\n" + "="*46)
    print("✅ MISSION ACCOMPLISHED: All agents successfully orchestrated.")
    print("🛡️  System Status: AUDITED | CODED | VERIFIED")
    print("="*46)

if __name__ == "__main__":
    main()