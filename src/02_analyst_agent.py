import os, re
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from jira import JIRA

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base_dir, '.env'))

def run_analyst_workflow():
    ticket_keys = []
    path = os.path.join(base_dir, "data", "security_audit_report.txt")
    if not os.path.exists(path): return []

    with open(path, "r") as file:
        requirements = [s.strip() for s in file.read().split('---') if len(s.strip()) > 20]

    llm = AzureChatOpenAI(azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"), api_key=os.getenv("AZURE_OPENAI_KEY"), azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"), api_version=os.getenv("AZURE_OPENAI_API_VERSION"))
    jira = JIRA(server=os.getenv("JIRA_SERVER"), basic_auth=(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN")))
    project_key = os.getenv("JIRA_PROJECT_KEY")

    for i, req in enumerate(requirements, start=1):
        system_msg = SystemMessage(content="""You are a Senior Security Product Manager. 
Analyze the following security audit finding and convert it into a formal Gherkin (Behavior-Driven Development) User Story.
Format your output EXACTLY like this:
TITLE: <A concise, 1-line summary of the security feature>
DESCRIPTION:
<Provide a brief context of the security flaw>
<Provide the formal Gherkin Syntax: Given... When... Then...>""")
        response = llm.invoke([system_msg, HumanMessage(content=req)])
        
        content = response.content.strip()
        title_match = re.search(r"TITLE:\s*(.*)", content, re.IGNORECASE)
        desc_match = re.search(r"DESCRIPTION:\s*(.*)", content, re.IGNORECASE | re.DOTALL)
        
        raw_title = title_match.group(1).strip() if title_match else "Security Remediation Task"
        details = desc_match.group(1).strip() if desc_match else content
        
        summary = f"SEC-{i}: {raw_title}"[:250]
        
        new_issue = jira.create_issue(fields={'project': {'key': project_key}, 'summary': summary, 'description': details, 'issuetype': {'name': 'Story'}}, prefetch=False)
        ticket_keys.append(new_issue.key)
        print(f"🎫 Created {new_issue.key}")

    return ticket_keys