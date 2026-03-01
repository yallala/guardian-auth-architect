# GUARDIAN-AUTH ARCHITECT
**From Strategic Advisor to AI Implementation Leader**

---

## 1. The Strategy (What We Are Building)

This system transforms a basic LLM workflow into a robust, enterprise-grade AI pipeline using Retrieval-Augmented Generation (RAG) and cloud-native infrastructure.

### The Problem Solved
Currently, the AI blindly generates code without knowing the company's internal rules. We are going to build a system that:
1. Embeds your Security Standards PDF into a FAISS Vector Database.
2. Forces the AI to read those standards (RAG) *before* it generates Jira tickets or code.
3. Automatically scaffolds the Cloud-Native infrastructure (Kubernetes YAML/Azure DevOps pipelines) needed to deploy it securely.

---

## 2. The 4-Week Execution Roadmap

This is our master checklist for building the end-to-end RAG architecture.

### Week 1: The Foundation (Setup & The Brain)
- [x] Install VS Code, Python, Git, and GitHub Copilot 
- [x] Set up Azure OpenAI & Jira API Keys 
- [ ] Build `src/vector_store.py`
  - [ ] Implement text/PDF extraction logic
  - [ ] Implement text chunking strategy
  - [ ] Set up FAISS index
  - [ ] Ingest simulated "Security Standards" document using OpenAI Embeddings
- [ ] Build `src/retrieve.py`
  - [ ] Prove semantic search capabilities (e.g., query "What are the MFA rules?")

### Week 2: Workflow A (The Analyst Agent)
- [x] Build `src/jira_connector.py`
  - [x] Establish ticket generation
- [ ] Build `src/agent_analyst.py`
  - [ ] Integrate RAG context retrieval 
  - [ ] Integrate GPT-4 API
- [ ] Implement Agentic Prompt Engineering 
  - [ ] Configure the prompt to enforce Gherkin syntax (Given/When/Then)
  - [ ] Configure the prompt to generate Edge Cases and Negative Testing scenarios
- [ ] Milestone: Run the full Analyst script and verify a complete User Story appears in Jira

### Week 3: Workflow B (The Architect Agent)
- [ ] Build `src/agent_architect.py`
  - [ ] Implement reading the Jira ticket payload via API
- [x] Build the File Generator
  - [x] Create Python source files (`.py`) automatically
- [ ] Implement the Infrastructure Layer (IaC)
  - [ ] Generate ARO `deployment.yaml` (Kubernetes Manifests)
  - [ ] Generate `azure-pipelines.yaml`
- [ ] Milestone: Run the script and verify a "Ready to Deploy" folder structure is cleanly generated 

### Week 4: The Enterprise Polish (Safety & Marketing)
- [ ] Implement Safety & Secrets
  - [ ] Build `src/safety_validator.py` (PII check simulation)
  - [ ] Build `src/secrets_manager.py` (Simulate Azure Key Vault)
- [ ] Implement Model Routing
  - [ ] Build `src/model_router.py` to route requests between standard models (GPT-4o) and reasoning models (o3-mini).
- [ ] The Demo Video
  - [ ] Record a 3-minute Loom video walking through architecture
- [ ] The Business Case
  - [ ] Write the "ROI & Risk" `README.md` for GitHub presentation
