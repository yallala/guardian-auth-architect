"""
AGENT: 02_analyst_agent.py (The Blueprint Architect)
ROLE: Converts security risks into step-by-step project tasks.
FLOW: Reads [security_audit_report.txt] -> Pushes tasks to Jira Cloud.
"""

import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from jira import JIRA

# 1. Setup paths and environment
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base_dir, '.env'))

def remediate_findings():
    print("🚀 Analyst Agent: Starting Blueprint Generation...")
    
    # 2. Read the Auditor's findings
    # UPDATED: Now looks for the new report name
    findings_path = os.path.join(base_dir, "data", "security_audit_report.txt")
    
    if not os.path.exists(findings_path):
        print(f"❌ Error: Could not find report at {findings_path}. Run 01_auditor_agent.py first!")
        return

    with open(findings_path, "r") as f:
        audit_report = f.read()
    
    print("✅ Security Audit Report loaded successfully.")

    # 3. Initialize AI and Jira
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

    # 4. Ask AI to create ATOMIC remediation stories with Indexing
    print("🧠 Decomposing Audit Findings into Numbered Security Stories...")
    
    system_prompt = SystemMessage(content="""
        You are a Minimalist Security Engineer.
        TASK: Convert the provided Audit Point into exactly ONE Atomic User Story.
        
        STRICT NAMING CONVENTION:
        The Story Title MUST start with 'Feature A.1'.
        
        RULES:
        1. Do NOT over-complicate. Focus only on the core requirement.
        2. Provide exactly 2 Acceptance Criteria and 1 simple Gherkin Scenario.
        
        STRICT FORMAT: 
        Output ONLY the story content. Do not add introductory text.
        Separate the title from the body clearly.
    """)
    
    response = llm.invoke([system_prompt, HumanMessage(content=audit_report)])

    # 5. Split and Upload to Jira
    remediation_stories = [s.strip() for s in response.content.split('###') if len(s.strip()) > 20]

    for i, story_content in enumerate(remediation_stories, start=1):
        # Extract the title from the first line
        first_line = story_content.split('\n')[0].replace('Title:', '').replace(f'Feature A.{i}:', '').strip()
        final_summary = f"Feature A.{i}: {first_line}"
        
        print(f"📤 Uploading Atomic Fix: {final_summary}...")

        jira.create_issue(
            project=project_key,
            summary=final_summary,
            description=story_content,
            issuetype={'name': 'Story'}
        )

    print(f"✅ SUCCESS! Generated {len(remediation_stories)} numbered remediation tickets.")

if __name__ == "__main__":
    remediate_findings()