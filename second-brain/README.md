# 🧠 AISDLC Second Brain (Knowledge Base & Project Documentation)

Welcome to the **AISDLC Second Brain**, the central hub for gathering, analyzing, and managing all information in this project through the AI Software Development Life Cycle (AISDLC).

---

## 📁 Directory Structure

This folder is designed to support structured and systematic document storage as follows:

### [📥 00-inbox](00-inbox/)

- **Goal**: Record raw requirements, meeting notes, client briefs, or initial ideation for development.

### [📝 10-requirements-spec](10-requirements-spec/)

- **Goal**: A repository for business requirements and system design specifications, divided into Core (central system) and individual feature/CR documents:
  - `system_spec.md` (Core System Specification): **The core system specification document serving as the Single Source of Truth** (consolidating all current system APIs and DB Schemas).
  - `features/<feature-id-slug>/`: Dedicated folders for each feature or CR to store the development artifacts for that cycle:
    - `brd.md` (Business Requirement Document): Created by `@pm-po` to define the goals, scope, and target users.
    - `epics_user_stories.md` (Epics, User Stories & Acceptance Criteria): Created by `@pm-po` to break down features into user stories with AC (Given-When-Then format).
    - `system_spec.md` (Feature System Specification): Created by `@sa` to describe technical specs specific to this feature.
- **Key Documents**: Core `system_spec.md` and feature-specific folders under `features/`.

### [📐 20-architecture](20-architecture/)

- **Goal**: System architecture analysis and impact assessment (Blast Radius Analysis):
  - `features/<feature-id-slug>/architecture_impact.md`: Created by `@solution-architect` to outline affected files and design API boundaries/contracts.
- **Key Documents**: Feature-specific folders under `features/`.

### [💻 30-development](30-development/)

- **Goal**: Coding guidelines and architectural standards for the project.
- **Key Documents**: `dev-guidelines.md`.

### [🛡️ 40-security](40-security/)

- **Goal**: Security audits and vulnerability scans (OWASP Top 10):
  - `features/<feature-id-slug>/security_audit.md`: Created by `@security` to outline scan findings and remediation steps.
- **Key Documents**: Feature-specific folders under `features/`.

### [🧪 50-qa-testing](50-qa-testing/)

- **Goal**: E2E quality assurance test planning and executions:
  - `features/<feature-id-slug>/test_plan.md`: Test plan designed by `@qa-automate`.
  - `features/<feature-id-slug>/test_execution.md`: Real execution logs recorded by `@qa-automate`.
- **Key Documents**: Feature-specific folders under `features/`.

### [🚀 60-delivery-ops](60-delivery-ops/)

- **Goal**: Deployment playbooks, environments details, release notes summaries, and incident reports (Post-Mortem Reports).

### [📚 70-resources](70-resources/)

- **Goal**: General manuals, cheat sheets, links to external docs, and shared knowledge bases.

---

## 🔄 AISDLC Workflow (Flat PM Architecture - Strategy B)

```mermaid
graph TD
    User([User Requirement]) -->|Write to Inbox Log| PM[pm-po]

    subgraph "Phase 0: Initiation"
        PM -->|1. Run init_feature.py --type| Init[Feature/CR/Bug Folders]
    end

    subgraph "Phase 1: Design & Analysis"
        Init -->|Check Type| TypeDecision{Type?}
        
        TypeDecision -->|Feature/CR| SA[sa]
        SA -->|2. Write BRD, Epics & Spec| Spec[Feature system_spec.md]
        Spec --> PM_Arch[PM Forwards Spec]
        PM_Arch --> Arch[solution-architect]
        
        TypeDecision -->|Bug Fix| BugArch[solution-architect]
        BugArch -->|2. Analyze Root Cause| BugDiag[bug_diagnosis.md]
        
        Arch -->|3. Analyze Impact| Impact[architecture_impact.md]
    end

    subgraph "Phase 2: Implementation"
        PM -->|4. Command Backend/Frontend implementation| Dev[backend-dev / frontend-dev]
        
        %% Feature/CR Flow
        Spec & Impact -.->|References| Dev
        PM -->|5. Command Test Plan design| QAP[qa-automate]
        QAP -->|6. Design Test Plan| TP[test_plan.md]
        
        %% Bug Flow
        BugDiag -.->|References for fixing| Dev
        
        Dev -->|7. Commit code and write Changelog| Code[Backend/Frontend Code]
    end

    subgraph "Phase 3: Verification"
        PM -->|8. Command E2E Test execution| QAA[qa-automate]
        QAA -->|9. Run E2E Test| Exec[test_execution.md]
        
        %% Feature/CR Flow Only
        PM -->|10. Command Security Audit| SE[security]
        SE -->|11. Scan for Vulnerabilities| Audit[security_audit.md]
    end

    subgraph "Phase 4: Release & Closure"
        PM -->|12. Merge spec changes to Core specs| Master[Core system_spec.md & api_contract.yaml]
        PM -->|13. Move Folder to Archives| Archive[archives/ folder]
    end

    PM -.->|Update Kanban board| PB[project_board.md]
    PM -.->|Update Master index| Idx[00-Index.md]
    PM -->|14. Summarize and notify results| User
```

This documentation acts as the project's "Second Brain", ensuring all AI agents in the development loop access consistent, up-to-date information, delivering high-standard and secure software.

---

## 🚀 How to Use the AISDLC Workflow for Developers (Human-AI Collaboration)

In this Multi-Agent system, the human developer's role is to provide initial inputs and verify outcomes:

### 1. Submitting Initial Requirements

To request a new feature or report a bug, append your requirements to the **very top (Top-append)** of [inbox_log.md](file://second-brain/00-inbox/inbox_log.md) following the template format:

- Date (YYYY-MM-DD)
- Type (Feature / Hotfix / Task)
- Detailed Requirements
- Initial Status: `Pending`

### 2. Triggering the PM-PO Agent

Invoke the `@pm-po` agent via CLI or your IDE. It will read `inbox_log.md` and orchestrate the specialist agents through each phase automatically.

### 3. Collaborating in the Loop

- **When Spec/Impact completes (Phase 1)**: Review `system_spec.md` and `architecture_impact.md` to ensure the AI's technical specifications match your expectations.
- **When Loop Protection triggers (Phase 2 & 3)**: If the security scan fails or E2E tests fail repeatedly more than twice, the PM-PO agent will pause execution and report back in the chat. You can review the logs, adjust the code, or revise specifications to unblock the flow.

---

## 💡 Creating Project-Specific Custom Skills

If you want to add custom coding guidelines or standards for agents to follow:

1. Create a new skill folder under [.agents/skills/](file://../.agents/skills/) (e.g., `my-project-coding-standard`).
2. Create a `SKILL.md` inside it with a YAML Frontmatter:
   ```yaml
   ---
   name: my-project-coding-standard
   description: Project-specific coding standards and guidelines for this service
   ---
   ```
3. Document your guidelines in Markdown inside that file.
4. Add the skill name to the `skills:` list in the corresponding agent files under [.gemini/agents/](file://../.gemini/agents/) (e.g., `backend-dev.md` or `frontend-dev.md`).

---

## 🧠 Karpathy's Second Brain Concepts in this Project

We adapted **Andrej Karpathy's** personal knowledge management principles to optimize team communication and documentation:

### 1. Append-and-Review (Frictionless Daily Logs)

- **Execution**: All raw requirements are recorded in `[[inbox_log]]`.
- **Gravity Rule**: New logs are appended at the top; older items sink to the bottom. Developers pull active entries into specific specs as needed, avoiding cognitive bloat and outdated noise.

### 2. LLM Wiki (AI-managed Wiki Network)

- **Execution**: AI agents use **Obsidian Wikilinks (`[[Filename#Section]]`)** to link documents across directories. This maintains an interconnected, dynamically linked knowledge graph.

### 3. Health Checks & Linting (Data Integrity Scanning)

- **Execution**: We use the [brain_linter.py](file://../scripts/brain_linter.py) script to scan documentation health:
  - Command: `python3 scripts/brain_linter.py`
  - It searches for **broken links** or **missing references** to ensure the AI's knowledge base remains consistent throughout the AISDLC workflow.
