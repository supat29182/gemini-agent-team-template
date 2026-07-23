# 🤖 Workspace Customization Rules (AGENTS.md)

This file defines the behavior rules, agreements, and workspace-level operational standards (Workspace Rules) for all AI Agents operating in this system to support the **AISDLC (AI Software Development Life Cycle)** process and maintain the reliability of the **Second Brain** knowledge base.

---

## 🔄 1. Collaborative Development Rules according to the AISDLC Process

The software development process in this Workspace is divided into 4 main phases, executed sequentially and always linked by documentation. The `@pm-po` acts as the main coordinator (Flat Orchestrator), directly delegating and tracking tasks with all Specialist Agents:

```
                  ┌───────────────────── pm-po ─────────────────────┐
                  │                       │                         │
                  ▼                       ▼                         ▼
          [PHASE 1: DESIGN]     [PHASE 2: IMPLEMENTATION]   [PHASE 3: VERIFICATION]
          (Sequential)          (Sequential/Parallel)       (Parallel Block)
          - sa (Spec)           - backend-dev  &            - security (Audit)
          - ux-ui (Design Spec)   qa-automate (Test Plan)   - qa-automate (E2E)
          - solution-architect  ── Sync Point 2 ──          ── Sync Point 3 ──
            (Impact Analysis)   - frontend-dev                     │
                                ── Sync Point 2.5 ──               ▼
                                                       [PHASE 4: POST-MORTEM]
                                                       - dev / solution-architect
                                                         (Lessons learned & Rule Compounding)
```

1.  **Do not skip workflow steps**: Work must always begin with the design phase. The development team is strictly prohibited from writing code before the system specification documents and architectural impact analysis are fully completed.
2.  **Scope of forwarded data**: Design data, code, and security audit results must be converted into documentation in the Second Brain so the team can utilize and reference them.
3.  **Feedback Loop Mechanism**:
    - If `@security` detects a vulnerability at the FAILED level in `[[security_audit]]`, send a report directly to `@pm-po` so the PM can send the task back to the Dev team to fix until it passes.
    - If `@qa-automate` detects a Bug during testing, send the bug logs and failed test reports back to `@pm-po` to assign a fix.
4.  **Parallel Coordination Mechanism**:
    - In Phase 2 and Phase 3, agents are executed in parallel, using decentralized lock files under the `locks/` folder inside the Feature/Bug directory as a state controller.
    - Agents running in parallel must lock their task (`in-progress`) by updating their individual lock file (e.g., `locks/<agent_name>.json`) before starting and unlock (`completed`) when finished.
    - Downstream agents (`@security`, `@qa-automate`) must verify that the lock file status of upstream tasks is "completed" before starting work.
    - `@pm-po` uses Sync Points to check the status in each lock file to transition between phases.
    - **Deadlock Timeout Rule (Deadlock Prevention):** `@pm-po` will check the `ttl_mins` value in each agent's lock file. If any task remains in an `in-progress` state longer than the defined `ttl_mins` (calculated from `locked_at` compared to the current time), it is immediately considered FAILED and unlocked to prevent system freezes (Infinite Wait).
5.  **Reflection Gate Mechanism**:
    - After successfully passing testing and verification in Phase 3, do not skip the lesson summary. Always proceed to **Phase 4: Post-Mortem & Reflection**.
    - The Specialist (Dev / Solution Architect) must write a Post-Mortem document following `template-postmortem.md` to summarize lessons learned and distill them into a one-line rule in `lessons_learned.md`.
6.  **Executive Summary Requirement for the PM**: Even though `@pm-po` acts as a Blind Orchestrator and is forbidden from reading full files, the executing Agent in each phase must always return a brief 3-4 line summary (Executive Summary) of the results to the Inbox or directly notify `@pm-po` upon task completion, allowing the PM to make an initial assessment before phase transition.

---

## 🧠 2. Second Brain Usage Rules and Standards

To ensure the "Second Brain" system functions as the project's knowledge base with maximum stability, adhere to the following rules:

1.  **Writing Links in Obsidian Wikilinks Format**:
    - All AI Agents must use Obsidian wikilink syntax `[[filename]]` or `[[filename#section]]` when referencing documents or specifications across categories.
    - _Do not_ specify filenames loosely without double square brackets.
2.  **Append-and-Review Rule in the Inbox**:
    - The `second-brain/01-inbox/inbox_log.md` (`[[inbox_log]]`) file will be used as the main task reception box.
    - When there is a new request, append it only to the **very top (Top-append)** of the LOGS, specifying the date, type, status, and a link to the results.
    - Avoid letting outdated records sink down without supervision. Regularly check and update statuses.
3.  **Project Board**:
    - The `second-brain/project_board.md` (`[[project_board]]`) file is strictly the Single Source of Truth for viewing the overall project status.
    - `@pm-po` must update the task status on this board every time a phase transition occurs. No Agent is allowed to remember the state (Context) on its own to prevent miscommunication issues.
4.  **Consistency of Main Document Paths**:
    - **System Spec**: `second-brain/03-requirements-spec/system_spec.md` (`[[system_spec]]`)
    - **API Contract**: `second-brain/03-requirements-spec/api_contract.yaml` (`[[api_contract]]`)
    - **Architecture Impact**: `second-brain/04-architecture/architecture_impact.md` (`[[architecture_impact]]`)
    - **Security Audit**: `second-brain/06-security/security_audit.md` (`[[security_audit]]`)
    - **Test Plan**: `second-brain/07-qa-testing/test_plan.md` (`[[test_plan]]`)
    - **Test Execution Log**: `second-brain/07-qa-testing/test_execution.md` (`[[test_execution]]`)

---

## 🛡️ 3. Quality & Safety Gates

1.  **Mandatory Data Health Check via Brain Linter**:
    - Every time a task concludes, the Agent must use `run_command` to execute `python3 scripts/brain_linter.py` to check document integrity within `second-brain/`:
    - If the output reveals Broken Links or data contradictions in the background system, the user or bot must immediately fix the links and content.
2.  **Security Engineer's Code Modifications**:
    - The `@security` bot is prohibited from modifying or writing core system code by itself to prevent Business Logic Broken issues.
    - Its duty is to analyze, detect risks, and specify remediation steps clearly in the `[[security_audit]]` report so the Dev can execute them.

---

## 💻 4. Execution and Code Verification Constraints

1.  **No Guessing Work Outcomes**:
    - The `@backend-dev`, `@frontend-dev`, `@ux-ui`, `@security`, and `@qa-automate` bots must not accept a task as complete without using the command execution tool (`run_command`) to run Unit Tests, Build the project, or execute scan scripts to verify functionality on the actual system.
2.  **Handling Bugs or Errors**:
    - When encountering issues during testing or build failures, thoroughly read the error logs in the Console and analyze consistency according to the sequence of requirements. If the specification is ambiguous, contact the PM immediately.

---

## 🤖 5. Agent Team Details and Roles (`.agents/agents/`)

This system orchestrates the collaboration of 9 Agents, whose configurations are saved in the [.agents/agents/](file://.agents/agents) directory, structuring operations via **Flat Orchestration** (no nesting) as follows:

### 1. PM/PO (`pm-po.md`)

- **Role**: The center and controller of the AISDLC process (Flat Orchestrator).
- **Critical Constraints**: **The PM/PO is strictly prohibited from writing or editing core project code, and must never draft technical specification documents themselves.** The PM/PO operates as a **Blind Orchestrator**, absolutely forbidden from using commands to read technical specification files (e.g., `system_spec.md`, `api_contract.yaml`) or any source code files on their own to review work (to save Tokens), and **must not memorize the project state on their own, always relying on the Project Board as the core.** The PM/PO only distributes Feature Slugs for Specialist Agents to read the files themselves.
- **Initial Input**: Read the latest requirements from `[[inbox_log]]` and the status from `[[project_board]]`.
- **Task Delegation**: Directly delegates tasks to each specialist agent according to the Phase (sa, ux-ui, solution-architect, backend-dev, frontend-dev, security, qa-automate).
- **Skills Used**: `using-agent-skills`, `context-engineering`, `idea-refine`, `interview-me`, `planning-and-task-breakdown`, `git-workflow-and-versioning`

### 2. System Analyst (`sa.md`)

- **Role**: Analyzes and drafts system specifications and designs the API Contract.
- **Input**: Task brief and `[[inbox_log]]` from `@pm-po`.
- **Output**: Writes the specifications into the `[[system_spec]]` file and drafts the `api_contract.yaml` as a mutual agreement, creates a wikilink back to the Inbox, and runs the brain linter.
- **Skills Used**: `spec-driven-development`, `obsidian-markdown`, `documentation-and-adrs`, `api-and-interface-design`, `interview-me`, `planning-and-task-breakdown`

### 3. UX/UI Designer (`ux-ui.md`)

- **Role**: ออกแบบ Wireframes, UI Component Specifications, Design Tokens และ User Flow Diagrams ในรูปแบบ text-based (`design_spec.md`)
- **Input**: Specifications จาก `[[system_spec]]` และ `[[epics_user_stories]]` (สั่งจาก `@pm-po`)
- **Output**: เขียน `design_spec.md` ที่ครอบคลุม Wireframe Descriptions, Component Specs, Design Tokens และ Interaction Guidelines ลงในโฟลเดอร์ Feature เพื่อเป็น Reference ให้ `@frontend-dev`
- **Critical Constraints**: **ห้ามเขียน Production Code (HTML/CSS/JS) ด้วยตัวเอง** หน้าที่คือออกแบบและสร้าง Visual Specification ในรูปแบบข้อความเท่านั้น
- **Skills Used**: `design-taste-frontend`, `frontend-ui-engineering`, `high-end-visual-design`, `brandkit`, `stitch-design-taste`, `obsidian-markdown`, `interview-me`

### 4. Solution Architect (`solution-architect.md`)

- **Role**: Designs the architecture and conducts impact analysis.
- **Input**: Reads from `[[system_spec]]` as commanded by `@pm-po`.
- **Output**: Uses `mcp_gitnexus_*` to analyze impacts, records them into `[[architecture_impact]]`, and runs the brain linter.
- **Skills Used**: `api-and-interface-design`, `documentation-and-adrs`, `doubt-driven-development`, `deprecation-and-migration`

### 5. Backend Developer (`backend-dev.md`)

- **Role**: Writes APIs, creates the Database Schema, and runs Backend Unit Tests.
- **Input**: Specifications from `[[system_spec]]`, API agreements from `api_contract.yaml` (as commanded by `@pm-po`).
- **Output**: Writes Server-side code referencing `api_contract.yaml`, ensures Unit Tests pass, writes changelog entries, and logs in the diary.
- **Skills Used**: `test-driven-development`, `incremental-implementation`, `source-driven-development`, `observability-and-instrumentation`, `code-simplification`, `debugging-and-error-recovery`, `custom-coding-standard`, `security-and-hardening`, `api-and-interface-design`

### 6. Frontend Developer (`frontend-dev.md`)

- **Role**: Designs and develops UI/UX and connects to Frontend APIs.
- **Input**: Specifications from `[[system_spec]]`, API agreements from `api_contract.yaml` (as commanded by `@pm-po`).
- **Output**: Writes Client-side code referencing `api_contract.yaml`, ensures the build passes, writes changelog entries, and logs in the diary.
- **Skills Used**: `design-taste-frontend`, `frontend-ui-engineering`, `test-driven-development`, `incremental-implementation`, `source-driven-development`, `code-simplification`, `debugging-and-error-recovery`, `custom-coding-standard`, `performance-optimization`, `browser-testing-with-devtools`, `api-and-interface-design`

### 7. Security Engineer (`security.md`)

- **Role**: Audits for security vulnerabilities in added/modified code.
- **Input**: Specifications from `[[system_spec]]` and current source code (as commanded by `@pm-po`).
- **Output**: Records the report findings into `[[security_audit]]`, specifying the file header as **[STATUS: PASSED]** or **[STATUS: FAILED]**, sent directly to `@pm-po`.
- **Skills Used**: `security-and-hardening`, `doubt-driven-development`, `code-review-and-quality`, `api-and-interface-design`

### 8. QA Automation Engineer (`qa-automate.md`)

- **Role**: Writes Test Plans and executes automated E2E test suites using Playwright MCP (incorporating Manual QA duties).
- **Input**: Specifications from `[[system_spec]]` (as commanded by `@pm-po`).
- **Output**: Drafts `[[test_plan]]` in Phase 2 and uses `mcp_playwright_*` to test on the actual system in Phase 3, recording the history into `[[test_execution]]` while truncating error logs to retain only the crucial substance up to 50 lines.
- **Skills Used**: `browser-testing-with-devtools`, `debugging-and-error-recovery`, `test-driven-development`, `ci-cd-and-automation`, `planning-and-task-breakdown`

### 9. Nexus Librarian (`nexus-librarian.md`)

- **Role**: The system's knowledge broker (Librarian), tasked with querying code structure and documentation via the GitNexus system.
- **Input**: Questions from other Agents invoking execution commands (e.g., `@pm-po`, `@sa`, `@backend-dev`).
- **Output**: In-depth code insights, system structures, or functional explanations along with File Paths sent back to the invoking Agent.
- **Skills Used**: `using-agent-skills` (with permissions to use GitNexus MCP)

---

## 🧠 6. Long-Term Memory (Tiered Architecture)

To conserve Tokens and prevent Context Bloat, AI Agents must adhere to the following reading order:

1. **Tier 1 (Mandatory)**: Always read `second-brain/00-Index.md` before starting work to view the project status.
2. **Tier 2 (Phase-Aware)**: Read only the documents relevant to the active Phase (e.g., if working on Phase 2, only read Spec and Impact) and read [[lessons_learned]] to learn about past mistakes or anti-patterns to avoid before designing or developing.
3. **Tier 3 (On-demand)**: Search for other documents or Archives only when necessary using search tools.

**Session Finalization Rules:**

- **Update 00-Index**: If a Phase transition is successful, update the AISDLC Phase Tracker in `00-Index.md`.
- **Diary Logging**: Record issues or pending task statuses into the `second-brain/11-diary/` folder.
- **Changelog Logging**: If code is modified, create a log entry in `second-brain/10-archives/changelog/` using the Template.
- **Post-Mortem & Reflection (Phase 4)**: Upon successful verification in Phase 3, record the Post-Mortem document following `template-postmortem.md` and extract brief summary lessons (One-Line Rule) to write updates into [[lessons_learned]].
- **Rule Compounding**: If a previous error or Anti-Pattern repeatedly occurs more than once, immediately update the strict rules (Never Do) section for that specific bot in [AGENTS.md](file://.agents/AGENTS.md) or the bot's system file to enforce it as mandatory behavior in the next cycle.

---

## 🏷️ 7. Templates & Tagging Policy

All AIs must comply with the tagging policy when creating new files (always specified in the YAML Frontmatter):

- **Do not create arbitrary document formats**: Use templates from `second-brain/09-resources/templates/`.
- **Tagging Policy**: Check `[[tagging-policy]]` (e.g., must include `#doc/spec` and `#phase/design`).

---

## 🌐 8. LLM Wiki Operations (The Compounding Strategy)

The knowledge base is akin to an evolving brain. AIs are responsible for maintaining this brain's condition continuously:

- **Ingest**: Whenever new information is obtained or a new file is created, always establish a Wikilink connecting the old page to the new one.
- **Lint**: Execute an integrity check using `run_command` to run `python3 scripts/brain_linter.py` before finalizing tasks to check for broken links.

---

## 📂 9. Path Reference Constraints

To enable smooth multi-user collaboration without broken links or missing files:

1. **Never specify Absolute Paths**: Do not use full paths containing specific Usernames or Directories, such as `file:///Users/username/...` or `/Users/username/...` in any specification document, config, or manual.
2. **Use Relative or Workspace-relative Paths**:
   - For standard links in documents, always use Relative paths, e.g., `../../.agents/skills/`.
   - Alternatively, use `file://.agents/skills/` so it can be opened regardless of whose computer is being used.
3. **Review before Committing**: Always double-check that no personal paths from your own machine have leaked into the project's source code and configuration.
4. **Task Delivery Block**: If absolute system paths are detected in any document (such as Changelogs, Diaries, or Source Code), it will be considered a FAILED level error. All agents are forbidden from reporting the task as finished or delivering it, and it must be corrected to pass the Linter every time.

---

## 💬 10. User Interaction & Interview Constraints

1. **Always ask one question at a time**: When needing to interview, gather requirements, or ask for consultation to clarify specs (e.g., using the approaches of `[[interview-me]]` or `[[idea-refine]]`), all AI Agents **must ask only 1 question at a time**. Sending a batch of questions simultaneously is prohibited, allowing the user to answer each point in detail.
2. **Attach hypotheses and confidence levels**: In each interview question, attach a hypothesis and Confidence Level (0-100%), specifying what is missing, to help the user clearly verify the direction.
3. **Correcting this behavior will instantly impact all AI Agents** to maintain a good user experience.

---

## 🚫 11. Anti-YOLO Mode Constraints

To prevent chaotic, risky executions, or causing system impact without screening, all AI Agents in the Workspace must adhere to the rules to disable "YOLO Mode" as follows:

1. **No Coding Without Spec**: Agents are strictly forbidden from guessing requirements on their own and writing code immediately without passing through the design process (Design Spec & Dev Plan) in the first phase.
2. **No Assumed Success**: Do not claim that development tasks are completed without actual testing via Build, Lint, or Test Runs, and do not ignore warnings/errors from the Compiler or Linter.
3. **No Bypass Quality Gates**: Agents are forbidden from delivering or committing work if the Brain Linter's health check or the Security Audit report returns a FAILED status.
4. **Doubt-Driven Check**: Agents must follow the `doubt-driven-development` skill to always question, challenge risk hypotheses, and find flaws in their own code before passing it on.
5. **Explicit User Permission**: Before an agent modifies/creates files or executes Terminal commands that affect the project, the agent must explain the goal, what will be modified, and the expected outcomes in the chat for the user's awareness, and always ask for approval/permission before actual execution. Silently modifying files or running background code without prior chat confirmation is prohibited.
6. **Mandatory Blast Radius Check**: It is strictly forbidden to edit any existing functions, classes, or architecture without sending a request to `@nexus-librarian` to run the `gitnexus_impact` tool to check for risks (Blast Radius / High Risk) beforehand.

## 🤖 12. GitNexus — Code Intelligence

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **gemini-agent-team-template** (498 symbols, 565 relationships, 2 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> If any GitNexus tool warns the index is stale, run `npx gitnexus analyze` in terminal first.

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `gitnexus_impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `gitnexus_detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `gitnexus_query({query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `gitnexus_context({name: "symbolName"})`.

## Never Do

- NEVER edit a function, class, or method without first running `gitnexus_impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `gitnexus_rename` which understands the call graph.
- NEVER commit changes without running `gitnexus_detect_changes()` to check affected scope.

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/gemini-agent-team-template/context` | Codebase overview, check index freshness |
| `gitnexus://repo/gemini-agent-team-template/clusters` | All functional areas |
| `gitnexus://repo/gemini-agent-team-template/processes` | All execution flows |
| `gitnexus://repo/gemini-agent-team-template/process/{name}` | Step-by-step execution trace |

## CLI

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |

<!-- gitnexus:end -->
