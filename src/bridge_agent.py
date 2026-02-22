import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from jira import JIRA

# 1. Setup paths and env
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base_dir, '.env'))

def remediate_findings():
    print("🚀 Bridge Agent: Starting Remediation Process...")
    
    # 2. Read the Auditor's findings
    findings_path = os.path.join(base_dir, "data", "audit_findings.txt")
    
    if not os.path.exists(findings_path):
        print(f"❌ Error: Could not find findings at {findings_path}. Run security_auditor.py first!")
        return

    with open(findings_path, "r") as f:
        audit_report = f.read()
    
    print("✅ Audit findings loaded successfully.")

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
        You are a Senior Security Engineer.
        Break the provided Audit Report into individual, ATOMIC User Stories.
        
        STRICT NAMING CONVENTION:
        Every Story Title MUST start with 'Feature A.x' (e.g., Feature A.1, Feature A.2).
        'A' stands for Audit.
        
        RULES:
        1. One story per specific security gap.
        2. Identify at least 2 critical edge cases per story.
        3. Provide EXACTLY 2-3 Acceptance Criteria and 1 Gherkin Scenario per story.
        
        STRICT FORMAT: Separate each story with the delimiter '###'.
    """)
    
    response = llm.invoke([system_prompt, HumanMessage(content=audit_report)])

    # 5. Split and Upload to Jira
    remediation_stories = [s.strip() for s in response.content.split('###') if len(s.strip()) > 20]

    for i, story_content in enumerate(remediation_stories, start=1):
        # Extract the title from the first line or use the index
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