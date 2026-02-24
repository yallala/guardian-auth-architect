import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from jira import JIRA

# Load configuration
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base_dir, '.env'))

def run_audit():
    # 1. Setup the AI & Jira
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

    # 2. Read requirements
    path = os.path.join(base_dir, "data", "requirements.txt")
    with open(path, "r") as file:
        content = file.read()

    print(f"🛡️ Security Auditor reviewing {project_key} context...")

    # 3. The Auditor's Persona
    system_msg = SystemMessage(content="""
        You are a Senior Cyber Security Architect.
        Produce a Structured Security Audit Report.
        
        FORMAT RULES:
        Separate distinct audit points with '---'.
        Separate individual Atomic Stories within those points with '###'.
        Titles must be concise.
    """)
    
    response = llm.invoke([system_msg, HumanMessage(content=content)])
    raw_findings = response.content
    
    # 4. IDEMPOTENCY FILTERING (The "Exact Match" Logic)
    # We split the report and check if Jira already has these stories
    print("🔍 Filtering findings against existing Jira backlog...")
    
    final_report = []
    points = raw_findings.split('---')
    
    for point in points:
        if "Title:" in point:
            # Extract the title line to check Jira
            try:
                title_line = [l for l in point.split('\n') if "Title:" in l][0]
                title = title_line.replace("Title:", "").strip()
                
                # JQL Exact Match Check
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

    # 5. Save only the NEW findings
    findings_path = os.path.join(base_dir, "data", "audit_findings.txt")
    with open(findings_path, "w") as f:
        f.write("\n---\n".join(final_report))

    print(f"✅ Audit complete. {len(final_report)} new findings saved to {findings_path}")

if __name__ == "__main__":
    run_audit()