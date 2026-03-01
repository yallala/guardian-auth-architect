"""
AGENT: 01_auditor_agent.py (The Safety Inspector)
ROLE: Scans raw ideas in the backlog for security risks.
FLOW: Reads [product_backlog.txt] -> Saves [security_audit_report.txt]
"""

import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from jira import JIRA

# Load configuration
# We find the project root so we can reach the /data and .env folders
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base_dir, '.env'))

def run_audit():
    # 1. Setup the AI & Jira connection
    llm = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_KEY")
    )

    jira = JIRA(
        server=os.getenv("JIRA_SERVER"),
        basic_auth=(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN"))
    )
    project_key = os.getenv("JIRA_PROJECT_KEY")

    # 2. Read requirements from the Product Backlog
    # UPDATED: Points to product_backlog.txt
    path = os.path.join(base_dir, "data", "product_backlog.txt")
    with open(path, "r") as file:
        content = file.read()

    print(f"🛡️ Security Auditor reviewing {project_key} context...")

    # 3. The Auditor's Persona (Instructing the AI how to think)
    
    system_msg = SystemMessage(content="""
    You are a Minimalist Security Auditor.
    TASK: Identify exactly ONE security audit point for the provided requirement.
    FORMAT: Title: [Title] --- Finding: [Finding] --- Recommendation: [Recommendation]
    """)
    
    response = llm.invoke([system_msg, HumanMessage(content=content)])
    raw_findings = response.content
    
    # 4. IDEMPOTENCY FILTERING (Don't repeat work already in Jira)
    print("🔍 Filtering findings against existing Jira backlog...")
    
    final_report = []
    points = raw_findings.split('---')
    
    for point in points:
        if "Title:" in point:
            try:
                title_line = [l for l in point.split('\n') if "Title:" in l][0]
                title = title_line.replace("Title:", "").strip()
                
                # JQL Exact Match Check: See if this title exists in Jira already
                jql = f'project = "{project_key}" AND summary ~ "\\"{title}\\""'
                existing = jira.search_issues(jql)
                
                if existing:
                    print(f"⏩ Already Tracking: '{title}' (Skipping from report)")
                    continue 
                else:
                    final_report.append(point)
            except Exception:
                final_report.append(point)
        else:
            final_report.append(point)

    # 5. Save only the NEW findings to the Security Audit Report
    # UPDATED: Now saves to security_audit_report.txt
    report_path = os.path.join(base_dir, "data", "security_audit_report.txt")
    with open(report_path, "w") as f:
        f.write("\n---\n".join(final_report))

    print(f"✅ Audit complete. {len(final_report)} new findings saved to {report_path}")

if __name__ == "__main__":
    run_audit()