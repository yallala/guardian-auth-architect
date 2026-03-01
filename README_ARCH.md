# 🏛️ The Guardian-Auth Data Flow: A Professional Relay Race

In this factory, no agent works in isolation. Each robot waits for the one before it to finish its report before starting. Here is exactly how the information flows through our system.

---

### 📥 Step 1: The Input
* **File:** `product_backlog.txt`
* **Purpose:** This is the "Wishlist." It contains the raw features we want to build.

---

### 🛡️ Step 2: The Security Audit
* **Agent:** `01_auditor_agent.py` (The Inspector)
* **Reads from:** `product_backlog.txt`
* **Saves to:** `security_audit_report.txt`
* **Logic:** The Inspector reads our wishlist and writes a formal report detailing every security danger it found.

---

### 📝 Step 3: The Project Planning
* **Agent:** `02_analyst_agent.py` (The Architect)
* **Reads from:** `security_audit_report.txt`
* **Saves to:** **Jira Cloud** (Digital Kanban Board)
* **Logic:** The Architect reads the Inspector's report and creates digital "Task Cards" in Jira so the team can track the progress.

---

### 💻 Step 4: The Construction
* **Agent:** `04_coder_agent.py` (The Builder)
* **Reads from:** **Jira Cloud**
* **Saves to:** `src/generated_code/` (The actual Python files)
* **Logic:** The Builder looks at the digital Task Cards in Jira and writes the actual software code, saving it into a specific folder.

---

### ⚖️ Step 5: The Final Exam
* **Agent:** `05_qa_tester_agent.py` (The Judge)
* **Reads from:** `src/generated_code/`
* **Output:** **Test Results** (Pass/Fail)
* **Logic:** The Judge looks at the code the Builder just finished and runs "stress tests" against it to make sure it doesn't break under pressure.

---

### 🕹️ The Overseer
* **File:** `main.py` (The Manager)
* **Role:** It sits in the middle, reading the status of every file and asking for your "Go/No-Go" approval before allowing the data to move from one file to the next.