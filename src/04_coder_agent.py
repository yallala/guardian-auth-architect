import os, re, textwrap
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from jira import JIRA

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base_dir, '.env'))

def build_feature(ticket_key):
    jira = JIRA(server=os.getenv("JIRA_SERVER"), basic_auth=(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN")))
    issue = jira.issue(ticket_key)
    gherkin = issue.fields.description
    
    llm = AzureChatOpenAI(azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"), api_key=os.getenv("AZURE_OPENAI_KEY"), azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"), api_version=os.getenv("AZURE_OPENAI_API_VERSION"))

    system_msg = SystemMessage(content="""You are a Senior Security Engineer. 
Write a complete, standalone Python file containing a class named `AccessLogic` that fulfills the given Gherkin User Story.
RULES:
1. Provide the FULL Python code. 
2. Keep the code EXTREMELY MINIMAL. Do NOT add any extra validation logic, security checks, or error handling.
3. For email, strictly write exactly this pattern:
   server = smtplib.SMTP(host, port)
   server.starttls()
   server.sendmail(sender, recipient, msg)
   server.quit()
4. Do not catch exceptions. Let them raise.
5. DO NOT write any execution code at the module level. Only define the `AccessLogic` class. Absolutely no code should run outside the class methods.
6. DO NOT import or use `dns.resolver`, `twilio`, `requests` or ANY external packages. Standard library ONLY.
7. Wrap your code exactly inside a ```python block.
""")
    
    response = llm.invoke([system_msg, HumanMessage(content=gherkin)])
    logic_match = re.search(r"```(?:python)?\n(.*?)\n```", response.content, re.DOTALL)
    
    if not logic_match:
        print(f"⚠️ Warning: LLM did not output proper python block for {ticket_key}. Using raw response.")
        logic_body = response.content
    else:
        logic_body = logic_match.group(1).strip()

    path = os.path.join(base_dir, "src", "generated_code", f"{ticket_key.replace('-', '_')}.py")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f: 
        f.write(logic_body)
    return True