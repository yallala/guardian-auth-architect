import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from jira import JIRA

# 1. Load configuration
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base_dir, '.env'))

def run_analyst_workflow():
    # --- STEP 1: READ REQUIREMENTS ---
    path = os.path.join(base_dir, "data", "requirements.txt")
    if not os.path.exists(path):
        print(f"❌ Error: Can't find {path}")
        return

    with open(path, "r") as file:
        # Skip the header and empty lines
        requirements = [line.strip() for line in file.readlines() if line.strip() and not line.startswith('Project:')]

    # --- STEP 2: INITIALIZE AI & JIRA ---
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

    # --- STEP 3: TRANSFORM TO GHERKIN & UPLOAD ---
    print(f"🚀 Converting {len(requirements)} rules into Gherkin Stories...")

    # Use 'enumerate' to get the index (1, 2, 3...) of each requirement
    for i, req in enumerate(requirements, start=1):
        print(f"🧠 Processing Feature {i} edge cases...")

        system_msg = SystemMessage(content=f"""
            You are a Senior Security Architect. 
            Requirement: {req}
            
            TASK:
            Break this into Atomic User Stories.
            
            STRICT NAMING CONVENTION:
            Every Story Title MUST start with 'Feature {i}.x' (e.g., Feature {i}.1, Feature {i}.2).
            
            FORMAT:
            Separate stories with '###'. 
            Each story needs: Title, 2 Criteria, and 1 Gherkin Scenario.
        """)
        
        response = llm.invoke([system_msg, HumanMessage(content=req)])
        atomic_stories = response.content.split('###')

        # Inner loop for the sub-features (1.1, 1.2...)
        for j, story in enumerate(atomic_stories, start=1):
            if len(story.strip()) > 20:
                summary_line = story.strip().split('\n')[0].replace('Title:', '').strip()
                # If the AI didn't follow naming perfectly, we force it here:
                final_summary = f"Feature {i}.{j}: {summary_line}"
                
                jira.create_issue(fields={
                    'project': {'key': project_key},
                    'summary': final_summary,
                    'description': story.strip(),
                    'issuetype': {'name': 'Story'},
                })
        
        
        response = llm.invoke([system_msg, HumanMessage(content=req)])

        # Split the AI's response into the individual atomic stories
        atomic_stories = response.content.split('###')

        for story in atomic_stories:
            if len(story.strip()) > 20:
                summary_line = story.strip().split('\n')[0].replace('Title:', '').strip()
                
                issue_dict = {
                    'project': {'key': project_key},
                    'summary': f'SEC-FEATURE: {summary_line}',
                    'description': story.strip(),
                    'issuetype': {'name': 'Story'},
                }
                new_issue = jira.create_issue(fields=issue_dict)
                print(f"🎫 Created Atomic Story: {new_issue.key}")
        
        response = llm.invoke([system_msg, HumanMessage(content=req)])

        # Create the ticket in Jira
        issue_dict = {
            'project': {'key': project_key},
            'summary': f'Feature: {req[:50]}',
            'description': response.content,
            'issuetype': {'name': 'Story'},
        }
        
        new_issue = jira.create_issue(fields=issue_dict)
        print(f"🎫 Created Gherkin Story: {new_issue.key}")

if __name__ == "__main__":
    print("🎬 Starting Analyst Agent...")
    run_analyst_workflow()