import os
import re
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from jira import JIRA

# 1. Setup paths and env
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base_dir, '.env'))

def sanitize_code(raw_content):
    """Strips AI chatter, markdown backticks, and conversational artifacts."""
    # 1. Remove Markdown code blocks
    code = raw_content.replace("```python", "").replace("```", "").strip()
    
    # 2. Filter out conversational lines that aren't Python code
    clean_lines = []
    chatty_keywords = ["here is", "this code", "requirement", "sure,", "i have", "note:", "steps:", "finally"]
    
    for line in code.splitlines():
        stripped = line.strip()
        if stripped.startswith(("#", "import", "from", "def", "class", "@", "if", "assert", "return", "pass")) or not stripped:
            clean_lines.append(line)
        elif line.startswith(("    ", "\t")):
            clean_lines.append(line)
        elif not any(word in stripped.lower() for word in chatty_keywords):
            if not re.match(r'^\d+\.', stripped):
                clean_lines.append(line)
            
    return "\n".join(clean_lines).strip()

def build_feature(jira, ticket_key):
    # --- 🚦 SMART SKIP LOGIC ---
    safe_name = ticket_key.replace("-", "_")
    logic_path = os.path.join(base_dir, "src", "generated_code", f"{safe_name}.py")
    test_path = os.path.join(base_dir, "src", "generated_code", f"test_{safe_name}.py")

    if os.path.exists(logic_path) and os.path.exists(test_path):
        print(f"⏩ Skipping {ticket_key}: Code and Test already exist locally.")
        return

    print(f"\n🛠️ Developer Agent: Starting build for {ticket_key}...")
    
    try:
        issue = jira.issue(ticket_key)
    except Exception as e:
        print(f"❌ Error: Could not find ticket {ticket_key} in Jira.")
        return

    gherkin_context = issue.fields.description if issue.fields.description else "No description provided."
    summary = issue.fields.summary

    # 2. Initialize AI
    llm = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_KEY")
    )

    # 3. Generate the Logic File
    # FIX: Renamed variable to system_msg_logic and added full rules
    system_msg_logic = SystemMessage(content="""
        You are a Senior Python Developer specializing in Cyber Security.
        RULES:
        1. Write clean, production-ready code.
        2. Use professional naming conventions (PEP8).
        3. Include comments explaining the security logic.
        4. Do not add any conversational text.
        5. Include a test case block at the bottom using 'if __name__ == "__main__":'.
        6. IMPORTANT: Return exact strings. Do not add periods at the end of messages.
    """)
    
    print(f"🧠 Generating Logic for {ticket_key}...")
    # FIX: Variable name now matches!
    logic_response = llm.invoke([system_msg_logic, HumanMessage(content=f"Requirement: {summary}\nGherkin: {gherkin_context}")])
    logic_code = sanitize_code(logic_response.content)

    # 4. Generate the Test File
    system_msg_test = SystemMessage(content=f"""
        You are a QA Engineer. Write a pytest file for the logic provided.
        RULES:
        1. Import the function from '{safe_name}'
        2. Write exactly 2 test cases.
        3. Use .strip() when comparing strings to ignore extra spaces or dots.
        4. Output ONLY valid Python code. No Markdown.
    """)
    
    print(f"🧪 Generating Pytest for {ticket_key}...")
    test_response = llm.invoke([system_msg_test, HumanMessage(content=f"Logic Code to test:\n{logic_code}")])
    test_code = sanitize_code(test_response.content)

    # 5. Saving Files
    os.makedirs(os.path.dirname(logic_path), exist_ok=True)

    with open(logic_path, "w") as f:
        f.write(logic_code)
    with open(test_path, "w") as f:
        f.write(test_code)

    print(f"✅ Saved Hardened Logic & Test for {ticket_key}")

if __name__ == "__main__":
    jira = JIRA(
        server=os.getenv("JIRA_SERVER"),
        basic_auth=(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN"))
    )
    project_key = os.getenv("JIRA_PROJECT_KEY")

    print(f"🔍 Searching for stories in {project_key}...")
    # Search for all stories that aren't finished
    issues = jira.search_issues(f'project={project_key} AND status != "Done"')

    if not issues:
        print("📭 No work found. Board is clean!")
    else:
        for issue in issues:
            build_feature(jira, issue.key)