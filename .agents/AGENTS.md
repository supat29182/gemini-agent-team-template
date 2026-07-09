# 🤖 Workspace Customization Rules (AGENTS.md)

ไฟล์นี้กำหนดกฎเกณฑ์พฤติกรรม ข้อตกลง และมาตรฐานการปฏิบัติงานระดับพื้นที่ทำงาน (Workspace Rules) สำหรับ AI Agents ทุกตัวที่เข้ามาดำเนินการในระบบนี้ เพื่อสนับสนุนกระบวนการ **AISDLC (AI Software Development Life Cycle)** และรักษาความน่าเชื่อถือของคลังความรู้ **Second Brain**

---

## 🔄 1. กฎการพัฒนาร่วมกันตามกระบวนการ AISDLC

กระบวนการพัฒนาซอฟต์แวร์ใน Workspace นี้แบ่งออกเป็น 4 เฟสหลัก ซึ่งดำเนินตามลำดับขั้นตอนและเชื่อมโยงกันด้วยเอกสารเสมอ โดยมี `@pm-po` ทำหน้าที่เป็นผู้ประสานงานหลัก (Flat Orchestrator) ที่สั่งการและติดตามงานกับ Specialist Agents ทุกตัวโดยตรง:

```
                  ┌───────────────────── pm-po ─────────────────────┐
                  │                       │                         │
                  ▼                       ▼                         ▼
          [PHASE 1: DESIGN]     [PHASE 2: IMPLEMENTATION]   [PHASE 3: VERIFICATION]
          (Sequential)          (Sequential/Parallel)       (Parallel Block)
          - sa (Spec)           - backend-dev  &            - security (Audit)
          - solution-architect    qa-automate (Test Plan)   - qa-automate (E2E)
            (Impact Analysis)   ── Sync Point 2 ──          ── Sync Point 3 ──
                                - frontend-dev                     │
                                ── Sync Point 2.5 ──               ▼
                                                       [PHASE 4: POST-MORTEM]
                                                       - dev / solution-architect
                                                         (Lessons learned & Rule Compounding)
```

1.  **ห้ามข้ามขั้นตอนการทำงาน**: การทำงานจะต้องเริ่มจากเฟสดีไซน์เสมอ ห้ามมิให้ทีมพัฒนาลงมือเขียนโค้ดก่อนที่เอกสารสเปกระบบและผลกระทบสถาปัตยกรรมจะเสร็จสมบูรณ์
2.  **ขอบเขตข้อมูลที่ส่งต่อ**: ข้อมูลการออกแบบ โค้ด และผลลัพธ์การตรวจสอบความปลอดภัยจะต้องถูกแปลงลงในเอกสารของ Second Brain เพื่อให้ทีมงานสามารถใช้ประโยชน์และอ้างอิงได้
3.  **กลไกแก้ไขงาน (Feedback Loop)**:
    - หาก `@security` ตรวจพบช่องโหว่ระดับ FAILED ใน `[[security_audit]]` ให้ส่งรายงานตรงไปยัง `@pm-po` เพื่อให้ PM ส่งงานกลับไปให้ทีม Dev แก้ไขจนกว่าจะผ่าน
    - หาก `@qa-automate` ตรวจพบ Bug ในระหว่างการทดสอบ ให้ส่ง Log บั๊กและรายงานการทดสอบที่ล้มเหลวกลับไปยัง `@pm-po` เพื่อสั่งการแก้ไขงาน
4.  **กลไกประสานงานคู่ขนาน (Parallel Coordination)**:
    - ใน Phase 2 และ Phase 3 มีการรันเอเจนต์แบบขนาน โดยใช้ไฟล์ `task_locks.json` ภายใน Feature Folder เป็นตัวควบคุมสถานะ
    - Agent ที่รันคู่ขนานต้องล็อกงาน (`in-progress`) ก่อนเริ่ม และปลดล็อก (`completed`) เมื่อเสร็จ
    - Agent ปลายน้ำ (`@security`, `@qa-automate`) ต้องตรวจสอบว่างาน upstream เสร็จสมบูรณ์ก่อนเริ่มทำงาน
    - `@pm-po` ใช้ Sync Points ตรวจสอบสถานะใน lock file เพื่อเปลี่ยน Phase
    - **กฎ Deadlock Timeout (ป้องกัน Deadlock):** `@pm-po` จะตรวจสอบค่า `ttl_mins` ของแต่ละ task ในไฟล์ `task_locks.json` หาก task ใดมีสถานะ `in-progress` นานเกินค่า `ttl_mins` ที่กำหนด (คำนวณจาก `locked_at` เทียบกับเวลาปัจจุบัน) ให้ถือว่า FAILED ทันทีและปลดล็อกเพื่อป้องกันระบบค้าง (Infinite Wait)
5.  **กลไกการสะท้อนคิด (Reflection Gate)**:
    - เมื่อผ่านการทดสอบและยืนยันใน Phase 3 เรียบร้อยแล้ว ห้ามข้ามการสรุปบทเรียน ให้ดำเนินการเข้าสู่ **Phase 4: Post-Mortem & Reflection** เสมอ
    - Specialist (Dev / Solution Architect) ต้องเขียนเอกสาร Post-Mortem ตาม `template-postmortem.md` เพื่อสรุปบทเรียนและกลั่นกรองออกมาเป็นกฎแบบบรรทัดเดียว (One-Line Rule) ลงใน `lessons_learned.md`
6.  **ข้อบังคับ Executive Summary ให้กับ PM**: แม้ว่า `@pm-po` จะมีสถานะเป็น Blind Orchestrator ห้ามอ่านไฟล์เต็ม แต่ Agent ผู้ปฏิบัติงานในแต่ละ Phase เมื่อส่งมอบงานเสร็จสิ้น จะต้องสรุปสาระสำคัญของผลลัพธ์แบบย่อ 3-4 บรรทัด (Executive Summary) กลับไปที่ Inbox หรือแจ้ง `@pm-po` โดยตรงเสมอ เพื่อให้ PM ประเมินผลเบื้องต้นก่อนเปลี่ยน Phase

---

## 🧠 2. ข้อบังคับและมาตรฐานการใช้งาน Second Brain

เพื่อให้ระบบ "สมองส่วนที่สอง" ทำหน้าที่เป็นคลังความรู้ของโครงการได้อย่างมีเสถียรภาพสูงสุด ให้ปฏิบัติตามกฎดังต่อไปนี้:

1.  **การเขียนลิงก์แบบ Obsidian Wikilinks**:
    - AI Agents ทุกตัวจะต้องใช้ไวยากรณ์วิกิลิงก์แบบ Obsidian `[[ชื่อไฟล์]]` หรือ `[[ชื่อไฟล์#หัวข้อ]]` ในการอ้างอิงเอกสารหรือข้อกำหนดระหว่างกันข้ามหมวดหมู่
    - _ห้าม_ ใช้วิธีระบุชื่อไฟล์แบบลอยๆ โดยไม่มีวงเล็บเหลี่ยมสองชั้น
2.  **กฎ Append-and-Review ใน Inbox**:
    - ไฟล์ `second-brain/00-inbox/inbox_log.md` (`[[inbox_log]]`) จะถูกใช้เป็นกล่องรับงานหลัก
    - เมื่อมีความต้องการใหม่ ให้เขียนต่อที่ **ด้านบนสุด (Top-append)** ของ LOGS เท่านั้น โดยระบุวันที่ ประเภท สถานะ และลิงก์เชื่อมโยงไปยังผลลัพธ์
    - หลีกเลี่ยงการปล่อยให้บันทึกที่ล้าสมัยจมลงไปโดยไม่มีผู้ดูแล ให้หมั่นตรวจสอบและอัปเดตสถานะ
3.  **กระดานติดตามสถานะ (Project Board)**:
    - ไฟล์ `second-brain/project_board.md` (`[[project_board]]`) เป็น Single Source of Truth อย่างเคร่งครัด สำหรับดูสถานะภาพรวมของโปรเจกต์
    - `@pm-po` จะต้องอัปเดตสถานะงานในกระดานนี้ทุกครั้งที่มีการข้าม Phase ห้าม Agent ตัวใดจดจำสถานะ (Context) ด้วยตนเองเพื่อป้องกันปัญหาการสื่อสารผิดพลาด
4.  **ความสอดคล้องของเส้นทางเอกสารหลัก**:
    - **System Spec**: `second-brain/10-requirements-spec/system_spec.md` (`[[system_spec]]`)
    - **API Contract**: `second-brain/10-requirements-spec/api_contract.yaml` (`[[api_contract]]`)
    - **Architecture Impact**: `second-brain/20-architecture/architecture_impact.md` (`[[architecture_impact]]`)
    - **Security Audit**: `second-brain/40-security/security_audit.md` (`[[security_audit]]`)
    - **Test Plan**: `second-brain/50-qa-testing/test_plan.md` (`[[test_plan]]`)
    - **Test Execution Log**: `second-brain/50-qa-testing/test_execution.md` (`[[test_execution]]`)

---

## 🛡️ 3. การควบคุมคุณภาพและความปลอดภัย (Quality & Safety Gates)

1.  **บังคับตรวจเช็คสุขภาพข้อมูลด้วย Brain Linter**:
    - ทุกครั้งที่จบงาน Agent ต้องใช้ `run_command` รัน `python3 scripts/brain_linter.py` เพื่อตรวจสอบความสมบูรณ์ของเอกสารใน `second-brain/`:
    - หากผลลัพธ์พบ Broken Links หรือความขัดแย้งของข้อมูล (Contradiction) ในระบบเบื้องหลัง ผู้ใช้หรือบอทจะต้องทำการแก้ไขลิงก์และเนื้อหาทันที
2.  **การแก้ไขโค้ดของ Security Engineer**:
    - บอท `@security` ห้ามทำการดัดแปลงหรือเขียนโค้ดระบบหลักด้วยตนเองเพื่อป้องกันปัญหาตรรกะระบบพัง (Business Logic Broken)
    - มีหน้าที่วิเคราะห์ ตรวจหาความเสี่ยง และระบุวิธีการแก้ไข (Remediation Steps) ลงในรายงาน `[[security_audit]]` ให้ชัดเจนเพื่อให้ Dev เป็นผู้ลงมือทำ

---

## 💻 4. ข้อบังคับด้านการรันคำสั่งและตรวจสอบโค้ดจริง (Execution Constraints)

1.  **ห้ามคาดเดาผลการทำงาน**:
    - บอท `@backend-dev`, `@frontend-dev`, `@security` และ `@qa-automate` ห้ามตอบรับว่างานเสร็จสิ้นหากยังไม่ได้ใช้เครื่องมือรันคำสั่ง (`run_command`) เพื่อทำการทดสอบ Unit Test, Build โครงการ หรือรันสคริปต์สแกนตรวจสอบการทำงานบนระบบจริง
2.  **การจัดการเมื่อพบบั๊กหรือ Error**:
    - เมื่อพบปัญหาระหว่างทดสอบหรือรันบิลด์ล้มเหลว ให้อ่าน Log ข้อผิดพลาดใน Console อย่างละเอียด และวิเคราะห์ความสอดคล้องตามลำดับความต้องการ หากสเปกคลุมเครือให้ติดต่อสอบถาม PM ทันที

---

## 🤖 5. รายละเอียดและบทบาทการทำงานของ Agent Team (`.agents/agents/`)

ระบบนี้ควบคุมการทำงานร่วมกันของ Agent 8 ตัวที่ถูกบันทึกคอนฟิกูเรชันไว้ในไดเรกทอรี [.agents/agents/](file://.agents/agents) ซึ่งจัดโครงสร้างการสั่งงานแบบ **Flat Orchestration** (ไม่มี nesting) ดังนี้:

### 1. PM/PO (`pm-po.md`)

- **บทบาท**: ศูนย์กลางและผู้ควบคุมกระบวนการ AISDLC (Flat Orchestrator)
- **ข้อจำกัดสำคัญ (Critical Constraints)**: **ห้าม PM/PO ดำเนินการเขียนหรือแก้ไขโค้ดโปรเจกต์หลัก และห้ามร่างเอกสารข้อกำหนดทางเทคนิคด้วยตนเองโดยเด็ดขาด** PM/PO มีฐานะเป็น **Blind Orchestrator** ห้ามใช้คำสั่งอ่านไฟล์สเปกเทคนิค (เช่น `system_spec.md`, `api_contract.yaml`) หรือไฟล์ซอร์สโค้ดใดๆ ด้วยตัวเองเพื่อตรวจสอบงานเด็ดขาด (เพื่อประหยัด Token) รวมถึง **ห้ามจดจำสถานะโปรเจกต์ด้วยตนเอง ต้องพึ่งพา Project Board เป็นแกนหลักเสมอ** PM/PO ทำหน้าที่แจก Feature Slug ให้ Specialist Agents ไปอ่านไฟล์เองเท่านั้น
- **อินพุตเริ่มต้น**: อ่านความต้องการล่าสุดจาก `[[inbox_log]]` และสถานะจาก `[[project_board]]`
- **การส่งงาน**: สั่งงานตรงไปยัง specialist agents แต่ละตัวตาม Phase (sa, solution-architect, backend-dev, frontend-dev, security, qa-automate)
- **ทักษะที่ใช้ (Skills)**: `using-agent-skills`, `context-engineering`, `idea-refine`, `interview-me`, `planning-and-task-breakdown`, `git-workflow-and-versioning`

### 2. System Analyst (`sa.md`)

- **บทบาท**: วิเคราะห์และจัดทำข้อกำหนดเฉพาะของระบบและออกแบบ API Contract
- **อินพุต**: บรีฟงานและ `[[inbox_log]]` จาก `@pm-po`
- **เอาต์พุต**: เขียนสเปกลงไฟล์ `[[system_spec]]` และร่าง `api_contract.yaml` เพื่อเป็นข้อตกลงร่วมกัน พร้อมทำวิกิลิงก์กลับหา Inbox และรัน brain linter
- **ทักษะที่ใช้ (Skills)**: `spec-driven-development`, `obsidian-markdown`, `documentation-and-adrs`, `api-and-interface-design`, `interview-me`, `planning-and-task-breakdown`

### 3. Solution Architect (`solution-architect.md`)

- **บทบาท**: ออกแบบสถาปัตยกรรมและวิเคราะห์ผลกระทบ
- **อินพุต**: อ่านจาก `[[system_spec]]` ตามคำสั่งของ `@pm-po`
- **เอาต์พุต**: ใช้ `mcp_gitnexus_*` วิเคราะห์ผลกระทบ บันทึกลงใน `[[architecture_impact]]` และรัน brain linter
- **ทักษะที่ใช้ (Skills)**: `api-and-interface-design`, `documentation-and-adrs`, `doubt-driven-development`, `deprecation-and-migration`

### 4. Backend Developer (`backend-dev.md`)

- **บทบาท**: เขียน APIs, จัดทำ Schema Database และรัน Unit Test ฝั่ง Backend
- **อินพุต**: สเปกจาก `[[system_spec]]`, ข้อตกลง API จาก `api_contract.yaml` (ตามคำสั่งของ `@pm-po`)
- **เอาต์พุต**: เขียนโค้ดฝั่ง Server อ้างอิงตาม `api_contract.yaml`, รัน Unit Test ให้ผ่าน, เขียน changelog entry และจด diary
- **ทักษะที่ใช้ (Skills)**: `test-driven-development`, `incremental-implementation`, `source-driven-development`, `observability-and-instrumentation`, `code-simplification`, `debugging-and-error-recovery`, `custom-coding-standard`, `security-and-hardening`, `api-and-interface-design`

### 5. Frontend Developer (`frontend-dev.md`)

- **บทบาท**: ออกแบบและพัฒนา UI/UX และเชื่อมต่อ API ฝั่ง Frontend
- **อินพุต**: สเปกจาก `[[system_spec]]`, ข้อตกลง API จาก `api_contract.yaml` (ตามคำสั่งของ `@pm-po`)
- **เอาต์พุต**: เขียนโค้ดฝั่ง Client อ้างอิงตาม `api_contract.yaml`, รัน build ให้ผ่าน, เขียน changelog entry และจด diary
- **ทักษะที่ใช้ (Skills)**: `frontend-ui-engineering`, `test-driven-development`, `incremental-implementation`, `source-driven-development`, `code-simplification`, `debugging-and-error-recovery`, `custom-coding-standard`, `performance-optimization`, `browser-testing-with-devtools`, `api-and-interface-design`

### 6. Security Engineer (`security.md`)

- **บทบาท**: ตรวจสอบช่องโหว่ความปลอดภัยของโค้ดที่เพิ่ม/แก้ไข
- **อินพุต**: สเปกจาก `[[system_spec]]` และซอร์สโค้ดปัจจุบัน (ตามคำสั่งของ `@pm-po`)
- **เอาต์พุต**: บันทึกรายงานผลลงใน `[[security_audit]]` โดยระบุหัวไฟล์เป็น **[STATUS: PASSED]** หรือ **[STATUS: FAILED]** ส่งตรงไปยัง `@pm-po`
- **ทักษะที่ใช้ (Skills)**: `security-and-hardening`, `doubt-driven-development`, `code-review-and-quality`, `api-and-interface-design`

### 7. QA Automation Engineer (`qa-automate.md`)

- **บทบาท**: เขียน Test Plan และรันชุดทดสอบ E2E อัตโนมัติด้วย Playwright MCP (รวบรวมหน้าที่ของ QA Manual เข้ามาด้วย)
- **อินพุต**: สเปกจาก `[[system_spec]]` (ตามคำสั่งของ `@pm-po`)
- **เอาต์พุต**: ร่าง `[[test_plan]]` ใน Phase 2 และใช้ `mcp_playwright_*` รันทดสอบระบบจริงใน Phase 3 พร้อมบันทึกประวัติลงใน `[[test_execution]]` โดยต้องตัดตอน Log ให้เหลือแต่สาระสำคัญไม่เกิน 50 บรรทัดเมื่อเกิด Error
- **ทักษะที่ใช้ (Skills)**: `browser-testing-with-devtools`, `debugging-and-error-recovery`, `test-driven-development`, `ci-cd-and-automation`, `planning-and-task-breakdown`

### 8. Nexus Librarian (`nexus-librarian.md`)

- **บทบาท**: บรรณารักษ์ข้อมูลประจำระบบ (Knowledge Broker) ทำหน้าที่สืบค้นโครงสร้างโค้ดและเอกสารผ่านระบบ GitNexus
- **อินพุต**: คำถามจาก Agent ตัวอื่นที่รันคำสั่งเรียกใช้งาน (เช่น `@pm-po`, `@sa`, `@backend-dev`)
- **เอาต์พุต**: ข้อมูลเชิงลึกของโค้ด โครงสร้างระบบ หรืออธิบายการทำงานพร้อมแนบ File Path ส่งกลับให้ Agent ที่เรียก
- **ทักษะที่ใช้ (Skills)**: `using-agent-skills` (พร้อมสิทธิ์ใช้งาน GitNexus MCP)

---

## 🧠 6. Long-Term Memory (Tiered Architecture)

เพื่อประหยัด Token และป้องกัน Context Bloat ให้ AI Agents ปฏิบัติตามลำดับการอ่านดังนี้:

1. **Tier 1 (Mandatory)**: อ่าน `second-brain/00-Index.md` เสมอก่อนเริ่มงาน เพื่อดูสถานะโปรเจกต์
2. **Tier 2 (Phase-Aware)**: อ่านเฉพาะเอกสารของ Phase ที่กำลังทำงาน (เช่น ทำ Phase 2 ก็ให้อ่านเฉพาะ Spec และ Impact) และอ่าน [[lessons_learned]] เพื่อเรียนรู้ข้อผิดพลาดหรือรูปแบบที่พึงหลีกเลี่ยง (Anti-Patterns) ก่อนทำการออกแบบหรือพัฒนา
3. **Tier 3 (On-demand)**: ค้นหาเอกสารอื่นๆ หรือ Archives เฉพาะเมื่อจำเป็นด้วยเครื่องมือค้นหา

**กฎการจบเซสชัน (Session Finalization):**

- **อัปเดต 00-Index**: หากเปลี่ยน Phase สำเร็จ ต้องอัปเดต AISDLC Phase Tracker ใน `00-Index.md`
- **บันทึก Diary**: บันทึกปัญหาหรือสถานะงานค้างลงในโฟลเดอร์ `second-brain/diary/`
- **บันทึก Changelog**: หากมีการแก้โค้ด ให้สร้างบันทึกใน `second-brain/archives/changelog/` โดยใช้ Template
- **ทำ Post-Mortem & Reflection (Phase 4)**: เมื่อผ่านการยืนยันใน Phase 3 สำเร็จ ต้องบันทึกเอกสาร Post-Mortem ตาม `template-postmortem.md` และสกัดบทเรียนสรุปสั้นๆ (One-Line Rule) ไปเขียนอัปเดตลงใน [[lessons_learned]]
- **ทำ Rule Compounding**: หากพบข้อผิดพลาดหรือ Anti-Pattern เดิมเกิดซ้ำซากมากกว่า 1 ครั้ง ให้ไปอัปเดตเพิ่มในหัวข้อกฎเหล็ก (Never Do) ของบอทตัวนั้นๆ ใน [AGENTS.md](file://.agents/AGENTS.md) หรือไฟล์ระบบของ Agent ตัวนั้นทันที เพื่อป้อนเป็นพฤติกรรมบังคับในรอบถัดไป

---

## 🏷️ 7. นโยบายการใช้เทมเพลตและแท็ก (Templates & Tagging)

AI ทุกตัวต้องปฏิบัติตามนโยบายการติดแท็กเมื่อสร้างไฟล์ใหม่ (ระบุใน YAML Frontmatter เสมอ):

- **ห้ามสร้างฟอร์แมตเอกสารมั่ว** ให้ดึงเทมเพลตจาก `second-brain/70-resources/templates/` มาใช้
- **นโยบายแท็ก**: ให้ตรวจสอบที่ `[[tagging-policy]]` (เช่น ต้องมี `#doc/spec` และ `#phase/design`)

---

## 🌐 8. LLM Wiki Operations (The Compounding Strategy)

คลังความรู้เปรียบเสมือนสมองที่เติบโตได้ AI มีหน้าที่รักษาสภาพสมองนี้ตลอดเวลา:

- **Ingest**: เมื่อได้ข้อมูลมาใหม่ หรือสร้างไฟล์ใหม่ ต้องสร้าง Wikilink เชื่อมจากหน้าเก่ามาหน้าใหม่เสมอ
- **Lint**: รันการตรวจสอบความสมบูรณ์โดยใช้ `run_command` รันคำสั่ง `python3 scripts/brain_linter.py` ทุกครั้งก่อนจบงาน เพื่อเช็คลิงก์เสีย

---

## 📂 9. กฎการระบุเส้นทางไฟล์ (Path Reference Constraints)

เพื่อให้โครงการสามารถทำงานร่วมกันได้หลายคน (Multi-user Collaboration) โดยไม่เกิดปัญหาลิงก์เสียหรือไฟล์หาไม่เจอ:

1. **ห้ามระบุ Absolute Path เด็ดขาด**: ห้ามใช้พาธแบบเต็มที่มีชื่อ User หรือ Directory เฉพาะเครื่อง เช่น `file:///Users/username/...` หรือ `/Users/username/...` ในเอกสารสเปก คอนฟิก หรือคู่มือใด ๆ
2. **ใช้ Relative Path หรือ Workspace-relative**:
   - สำหรับลิงก์มาตรฐานในเอกสาร ให้ระบุแบบ Relative เสมอ เช่น `../../.agents/skills/`
   - หรือใช้ `file://.agents/skills/` เพื่อให้สามารถเปิดอ่านได้ไม่ว่าจะอยู่ในเครื่องคอมพิวเตอร์ของใครก็ตาม
3. **ตรวจสอบก่อน Commit**: ตรวจทานเสมอว่าไม่มีพาธส่วนตัวของเครื่องตัวเองหลุดเข้าไปในซอร์สโค้ดและคอนฟิกูเรชันของโปรเจกต์
4. **การบล็อกการส่งมอบงาน**: หากตรวจพบพาธระบบแบบ Absolute ในเอกสารใด ๆ (เช่น บันทึก Changelog, Diary, หรือ Source Code) จะถือเป็นข้อผิดพลาดระดับ FAILED ห้ามเอเจนต์ทุกตัวรายงานว่างานเสร็จสิ้นหรือส่งมอบงานเด็ดขาด และต้องแก้ไขให้ผ่าน Linter ก่อนทุกครั้ง

---

## 💬 10. ข้อบังคับในการสัมภาษณ์และตอบโต้กับผู้ใช้ (User Interaction & Interview Constraints)

1. **ถามทีละหนึ่งคำถามเสมอ**: เมื่อต้องการสัมภาษณ์ รวบรวมความต้องการ หรือขอคำปรึกษาเพื่อความชัดเจนของสเปก (เช่น การใช้แนวทางของ `[[interview-me]]` หรือ `[[idea-refine]]`) AI Agents ทุกตัว **จะต้องตั้งคำถามครั้งละ 1 ข้อเท่านั้น** ห้ามส่งเป็นชุดคำถามพร้อมกันหลายข้อ เพื่อให้ผู้ใช้สามารถตอบได้ทีละประเด็นอย่างละเอียด
2. **แนบสมมติฐานและระดับความมั่นใจ**: ในการสัมภาษณ์แต่ละข้อ ต้องแนบสมมติฐาน (Hypothesis) และระดับความมั่นใจ (Confidence Level: 0-100%) พร้อมระบุสิ่งที่ขาดไป เพื่อช่วยให้ผู้ใช้ตรวจสอบทิศทางได้ชัดเจน
3. **การแก้ไขพฤติกรรมนี้จะส่งผลต่อ AI Agents ทุกตัวทันที** เพื่อรักษาประสบการณ์ใช้งานที่ดี

---

## 🚫 11. กฎป้องกันการทำงานแบบเสี่ยงอันตราย (Anti-YOLO Mode Constraints)

เพื่อป้องกันการทำงานที่ไร้ระเบียบ มีความเสี่ยง หรือการสร้างผลกระทบต่อระบบโดยไม่ผ่านการกลั่นกรอง ให้ AI Agents ทุกตัวใน Workspace ปฏิบัติตามกฎเพื่อปิดการทำงานแบบ "YOLO Mode" ดังนี้:

1. **ห้ามเขียนโค้ดโดยไม่มี Spec รองรับ (No Coding Without Spec)**: ห้ามเอเจนต์เดาความต้องการเองและลงมือเขียนโค้ดทันทีโดยไม่ผ่านกระบวนการออกแบบ (Design Spec & Dev Plan) ในเฟสแรกเด็ดขาด
2. **ห้ามเดาว่าโค้ดทำงานได้ (No Assumed Success)**: ห้ามเคลมว่าพัฒนางานเสร็จสิ้นหากไม่ได้มีการทดสอบจริงผ่านการ Build, Lint หรือ Test Run และห้ามละเลยคำเตือน (Warnings/Errors) จาก Compiler หรือ Linter
3. **ห้ามละเว้นระบบความปลอดภัย (No Bypass Quality Gates)**: ห้ามเอเจนต์ส่งมอบหรือ commit งานหากการตรวจสุขภาพระบบของ Brain Linter หรือรายงาน Security Audit ปรากฏผลลัพธ์เป็น FAILED
4. **การตรวจสอบยืนยันเชิงรุก (Doubt-Driven Check)**: ให้เอเจนต์ทำตามทักษะ `doubt-driven-development` เพื่อตั้งคำถาม ท้าทายสมมติฐานความเสี่ยง และหาจุดบกพร่องของโค้ดตนเองก่อนส่งต่อเสมอ
5. **ต้องขออนุญาตก่อนดำเนินงานเสมอ (Explicit User Permission)**: ก่อนที่เอเจนต์จะทำการแก้ไข/สร้างไฟล์ หรือเรียกใช้คำสั่ง Terminal ที่ส่งผลกระทบต่อโปรเจกต์ เอเจนต์ต้องอธิบายเป้าหมาย สิ่งที่จะแก้ไข และผลลัพธ์ที่คาดว่าจะเกิดขึ้นในแชทให้ผู้ใช้รับทราบ และขอความเห็นชอบ/ขออนุญาตก่อนลงมือปฏิบัติจริงเสมอ ห้ามทำการแก้ไขไฟล์เงียบๆ หรือรันโค้ดเบื้องหลังโดยไม่มีการยืนยันในแชทล่วงหน้า
6. **บังคับประเมินผลกระทบ (Mandatory Blast Radius Check)**: ห้ามแก้ไขฟังก์ชันคลาสหรือสถาปัตยกรรมใดๆ ที่มีอยู่เดิม โดยไม่ส่งคำร้องให้ `@nexus-librarian` รันเครื่องมือ `gitnexus_impact` เพื่อเช็คความเสี่ยง (Blast Radius / High Risk) ล่วงหน้าเด็ดขาด

## 🤖 12. GitNexus — Code Intelligence

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **gemini-agent-team-template** (294 symbols, 319 relationships, 2 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

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
