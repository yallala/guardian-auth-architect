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
        
        # Call the AI once per requirement
        response = llm.invoke([system_msg, HumanMessage(content=req)])
        atomic_stories = response.content.split('###')

        # Process the AI-generated stories
        for j, story_text in enumerate(atomic_stories, start=1):
            story_text = story_text.strip()
            
            # Ensure the segment actually contains a story
            if len(story_text) > 20:
                # Extract the first line as the title and clean it
                summary_line = story_text.split('\n')[0].replace('Title:', '').strip()
                final_summary = f"Feature {i}.{j}: {summary_line}"
                
                    # --- IDEMPOTENCY CHECK (EXACT MATCH) ---
                # We use '=' for an exact string match of the final summary
                jql = f'project = "{project_key}" AND summary ~ "\\"{final_summary}\\""'
                existing_issues = jira.search_issues(jql)

                if existing_issues:
                    print(f"⏩ Skipping: '{final_summary}' (Already exists as {existing_issues[0].key})")
                else:
                    # --- CREATION ---
                    print(f"🆕 Creating: '{final_summary}'")
                    new_issue = jira.create_issue(fields={
                        'project': {'key': project_key},
                        'summary': final_summary,
                        'description': story_text,
                        'issuetype': {'name': 'Story'},
                    })
                    print(f"🎫 Ticket Created: {new_issue.key}")

    print("\n✨ All requirements processed. Backlog is synchronized!")

if __name__ == "__main__":
    print("🎬 Starting Analyst Agent...")
    run_analyst_workflow()