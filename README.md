# GuardianAuth: Enterprise Agentic Security Platform

## 🛡️ Project Vision
GuardianAuth is an AI-Native platform that automates the generation of secure software by bridging the gap between static security policies and production code. It uses the **Login Feature** as a primary demonstration of end-to-end security automation.

## ⚙️ Core Workflows

### Workflow A: The Analyst (Compliance & Edge Case Engine)
* **Input**: Security Standards (PDF via RAG) + Application Design Specs.
* **Action**: Analyzes requirements against corporate security policies.
* **Output**: Generates a **Jira User Story** for the **Login Feature**, complete with mandatory security acceptance criteria and negative testing edge cases.

### Workflow B: The Developer (Cloud-Native Scaffolder)
* **Input**: Approved Jira Ticket from Workflow A.
* **Action**: Generates production-ready code and infrastructure.
* **Output**: Python source code, **ARO (OpenShift)** manifests, and **Azure DevOps** pipelines for the Login implementation.

## 🛠️ Technology Stack
* **Intelligence**: Azure OpenAI (GPT-4o), LangChain, FAISS (Vector DB).
* **Infrastructure**: Azure Red Hat OpenShift (ARO), Kubernetes, Docker.
* **Integration**: Jira REST API, GitHub Copilot.

## 👤 Architect
**Sudheer Kumar Yallalacheruvu**
*AI Implementation Leader | Enterprise Solutions Architect*