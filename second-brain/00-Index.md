# 🧠 00-Index (Master Hub)

> [!IMPORTANT]
> This page is the starting point and **Single Source of Truth** for all AI Assistants in this project.
> **Every AI must check this file before starting work** to check the current project status and track the AISDLC Phase.

---

## 🎯 AISDLC Phase Tracker

| Current Phase                         | Main Related Files                                                                                            |
| :------------------------------------ | :------------------------------------------------------------------------------------------------------------ |
| [ ] Inbox/Initiation                   | [[inbox_log]], [[project_board]]                                                                              |
| [ ] Phase 1: Design                    | [[system_spec]], [[architecture_impact]]                                                                      |
| [ ] Phase 2: Implementation            | Source Code, [[security_audit]]                                                                               |
| [ ] Phase 3: Verification              | [[test_plan]], [[test_execution]]                                                                             |
| [ ] Phase 4: Post-Mortem & Reflection | [[lessons_learned]], [[template-postmortem]]                                                                  |

_At the end of each Phase, AI or PM/PO should update the checkbox `[x]` here and advance the status to the next Phase._

---

## 📂 Project Directory

- **📥 01-Inbox**: Raw task inbox and initial assessment ➔ [[inbox_log]]
- **🧠 02-Knowledge Base**: Accumulated knowledge base and lessons learned ➔ [[lessons_learned]]
- **📝 03-Requirements**: System documentation and User Journey ➔ [[system_spec]]
- **📐 04-Architecture**: Design and impact assessment ➔ [[architecture_impact]]
- **💻 05-Development**: Developer workspace and coding guidelines ➔ [[dev-guidelines]]
- **🛡️ 06-Security**: Audit reports and OWASP ➔ [[security_audit]]
- **🧪 07-QA**: Test plans and results ➔ [[test_plan]], [[test_execution]]
- **🚀 08-Delivery**: Preparation for Production release ➔ [[deployment-playbook]]
- **📚 09-Resources**: Manuals, Templates, and policies ➔ [[tagging-policy]]
- **🗄️ 10-Archives**: History and old Changelogs ➔ `second-brain/10-archives/changelog/`
- **📓 11-Diary**: AI work logs ➔ `second-brain/11-diary/`

---

## ⚙️ Quick Rules

1. **Always read 00-Index**
2. **Use `[[wikilinks]]` for referencing every time**
3. **Do not modify code arbitrarily without updating the Spec first**
4. **Log reflections in Post-Mortem when errors occur or upon task completion**
5. **Log a Diary at the end of every work session** (if there are significant changes)

See all detailed rules at [[AGENTS]] or the `.agents/AGENTS.md` file
