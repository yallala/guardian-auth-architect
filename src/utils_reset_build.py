"""
UTILITY: utils_reset_build.py (The Janitor)
PURPOSE: Wipes 'generated_code' and truncates 'security_audit_report.txt' (clears text, keeps file).
RELATIONSHIP: Sits in src/ and prepares the environment for the 01_auditor_agent.py.
"""

import os
import shutil

def reset_build():
    # 1. Setup Absolute Paths (Ensures it works from any folder)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    generated_code_dir = os.path.join(script_dir, "generated_code")
    audit_report = os.path.join(project_root, "data", "security_audit_report.txt")
    
    print(f"🧹 Starting Nuclear Cleanup...")

    # --- Task A: Clear Local Generated Code (Delete Files) ---
    if os.path.exists(generated_code_dir):
        files = os.listdir(generated_code_dir)
        if not files:
            print("✅ 'generated_code' folder was already empty.")
        for filename in files:
            file_path = os.path.join(generated_code_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    print(f"🗑️ Deleted Code: {filename}")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f"📂 Deleted Folder: {filename}")
            except Exception as e:
                print(f"❌ Error deleting {filename}: {e}")
    else:
        os.makedirs(generated_code_dir)
        print(f"📁 Created missing directory: {generated_code_dir}")

    # --- Task B: Clear Stale Audit Report (Truncate Text, Keep File) ---
    if os.path.exists(audit_report):
        try:
            # Opening in 'w' mode empties the file without deleting it
            with open(audit_report, 'w') as f:
                f.write("") 
            print(f"🧹 Cleared contents of: security_audit_report.txt")
        except Exception as e:
            print(f"❌ Error clearing report: {e}")
    else:
        # If it doesn't exist, create it so the structure is ready
        try:
            with open(audit_report, 'w') as f:
                f.write("")
            print("📝 Created empty placeholder: security_audit_report.txt")
        except Exception as e:
            print(f"❌ Could not create placeholder: {e}")

    print("✨ Build environment is now 100% CLEAN.")

if __name__ == "__main__":
    reset_build()