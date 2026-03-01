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
        system_msg = SystemMessage(content="TASK: Convert audit to Title: [Short] ### Details: [Gherkin]. Keep Title on ONE line.")
        response = llm.invoke([system_msg, HumanMessage(content=req)])
        
        parts = response.content.split('###')
        # Fix: Ensure title is only the first line and stripped of newlines
        raw_title = parts[0].replace('Title:', '').strip().split('\n')[0] 
        details = parts[1] if len(parts) > 1 else response.content
        
        # Truncation + Newline Guard for Jira API
        summary = f"SEC-{i}: {raw_title}".replace('\n', ' ').strip()[:250]
        
        new_issue = jira.create_issue(fields={'project': {'key': project_key}, 'summary': summary, 'description': details, 'issuetype': {'name': 'Story'}}, prefetch=False)
        ticket_keys.append(new_issue.key)
        print(f"🎫 Created {new_issue.key}")

    return ticket_keys