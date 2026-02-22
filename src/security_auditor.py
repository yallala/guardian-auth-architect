import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
# UPDATED IMPORTS FOR NEW LANGCHAIN VERSIONS:
from langchain_core.messages import HumanMessage, SystemMessage

# Load env from the root
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base_dir, '.env'))

def run_audit():
    # 1. Setup the AI
    llm = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_KEY")
    )

    # 2. Path to our requirements
    path = os.path.join(base_dir, "data", "requirements.txt")
    with open(path, "r") as file:
        content = file.read()

    print("🛡️ Security Auditor is reviewing the project...")

    # 3. The Auditor's "Persona"
   # 3. The Auditor's "Persona" (Updated for Clean Organization)
    system_msg = SystemMessage(content="""
        You are a Senior Cyber Security Architect (CISA & CISSP certified).
        Your task is to produce a Structured Security Audit Report.
        
        ORGANIZE YOUR RESPONSE AS FOLLOWS:
        
        # [Heading: Audit Point Name]
        
        ## 📋 Requirement Context
        - **Source Requirement**: [Mention which original rule this relates to]
        - **Security Domain**: [e.g., Data Privacy, Access Control, or Auditability]
        
        ## 🚨 Identified Gap
        - Provide a clear, 1-sentence description of the vulnerability.
        
        ## 🛠️ Remediation Strategy (Atomic Stories)
        Separate each recommended fix with the delimiter '###' so the Bridge Agent can split them.
        For each fix, include:
        1. **Title**: [Action-oriented title]
        2. **Acceptance Criteria**: [Exactly 2 bullet points]
        3. **Gherkin Scenario**: [Given/When/Then]
        4. Make sure Feature Title starts with same 
        
        ---
        (Repeat the above structure for at least 3 distinct audit points)
    """)
    human_msg = HumanMessage(content=content)
    
    # --- THIS WAS THE MISSING LINE ---
    # We call the 'llm' and store the result in the variable 'response'
    response = llm.invoke([system_msg, human_msg])
    # ---------------------------------
    
    # 4. Save the findings to the data folder
    findings_path = os.path.join(base_dir, "data", "audit_findings.txt")
    with open(findings_path, "w") as f:
        f.write(response.content)

    print(f"✅ Audit complete. Findings saved to {findings_path}")

    print("\n🚨 SECURITY AUDIT REPORT 🚨")
    print("-" * 30)
    print(response.content)
    print("-" * 30)

if __name__ == "__main__":
    run_audit()