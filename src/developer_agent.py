import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from jira import JIRA

# 1. Setup paths and env
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base_dir, '.env'))

def build_feature(ticket_key):
    print(f"🛠️ Developer Agent: Starting build for {ticket_key}...")

    # 2. Connect to Jira
    jira = JIRA(
        server=os.getenv("JIRA_SERVER"),
        basic_auth=(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN"))
    )
    
    try:
        issue = jira.issue(ticket_key)
    except Exception as e:
        print(f"❌ Error: Could not find ticket {ticket_key}. check the ID!")
        return

    # Extract requirements from the Jira description
    gherkin_context = issue.fields.description if issue.fields.description else "No description provided."
    summary = issue.fields.summary

    print(f"📖 Reading Gherkin requirements from Jira...")

    # 3. Initialize AI
    llm = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_KEY")
    )

    # 4. The Developer's Persona
    system_msg = SystemMessage(content="""
        You are a Senior Python Developer specializing in Cyber Security.
        Your task is to write a clean, production-ready Python function based on the provided Gherkin scenario.
        
        RULES:
        1. Only output valid Python code. 
        2. DO NOT include Markdown formatting (like ```python) in your response. Start directly with the code.
        3. Include comments explaining the security logic.
        4. Use professional PEP8 naming conventions.
        5. Include a test case block at the bottom using 'if __name__ == "__main__":'.
    """)

    prompt = f"Ticket Summary: {summary}\nRequirements/Gherkin:\n{gherkin_context}"
    
    print(f"🧠 Generating Python code for {summary}...")
    response = llm.invoke([system_msg, HumanMessage(content=prompt)])
    
    # 5. Sanitization & Saving
    code_content = response.content

    # Logic to strip Markdown backticks if the AI provides them anyway
    if code_content.startswith("```"):
        # Removes the opening ```python or ``` and the closing ```
        lines = code_content.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:] # Remove first line
        if lines[-1].startswith("```"):
            lines = lines[:-1] # Remove last line
        code_content = "\n".join(lines)

    code_content = code_content.strip()

    # Create a clean filename
    safe_name = ticket_key.replace(".", "_").replace("-", "_")
    output_path = os.path.join(base_dir, "src", "generated_code", f"{safe_name}.py")

    with open(output_path, "w") as f:
        f.write(code_content)

    print(f"✅ SUCCESS! Code generated and saved to: {output_path}")

if __name__ == "__main__":
    # Update this to whichever ticket you want to build!
    target_ticket = "SEC-67" 
    build_feature(target_ticket)