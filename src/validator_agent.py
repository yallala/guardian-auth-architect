import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from jira import JIRA

# 1. Setup
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base_dir, '.env'))

def validate_feature(ticket_key):
    print(f"⚖️ Validator Agent: Auditing {ticket_key}...")

    # 2. Get the "Contract" from Jira
    jira = JIRA(
        server=os.getenv("JIRA_SERVER"),
        basic_auth=(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN"))
    )
    issue = jira.issue(ticket_key)
    gherkin = issue.fields.description

    # 3. Get the "Implementation" from your local file
    safe_name = ticket_key.replace(".", "_").replace("-", "_")
    code_path = os.path.join(base_dir, "src", "generated_code", f"{safe_name}.py")
    
    if not os.path.exists(code_path):
        print(f"❌ Error: No code found for {ticket_key} at {code_path}")
        return

    with open(code_path, "r") as f:
        source_code = f.read()

    # 4. Initialize AI to write the Test
    llm = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_KEY")
    )

    system_msg = SystemMessage(content="""
        You are a Senior QA Automation Engineer.
        ... (keep existing rules) ...
        3. Output ONLY the Python test code. No conversation.
        4. IMPORTANT: Use .strip() when comparing strings to ignore extra spaces or dots.
    """)

    prompt = f"GHERKIN REQUIREMENTS:\n{gherkin}\n\nSOURCE CODE:\n{source_code}"
    
    print(f"🧪 Generating automated tests for {ticket_key}...")
    response = llm.invoke([system_msg, HumanMessage(content=prompt)])

    # 5. Save the Test file
    test_path = os.path.join(base_dir, "src", "generated_code", f"test_{safe_name}.py")
    with open(test_path, "w") as f:
        f.write(response.content.replace("```python", "").replace("```", "").strip())

    print(f"✅ SUCCESS! Test suite created: {test_path}")
    print(f"👉 Run it with: pytest {test_path}")

if __name__ == "__main__":
    validate_feature("SEC-67")