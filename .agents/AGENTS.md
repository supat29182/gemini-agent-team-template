# 🤖 Workspace Customization Rules (AGENTS.md)

ไฟล์นี้กำหนดกฎเกณฑ์พฤติกรรม ข้อตกลง และมาตรฐานการปฏิบัติงานระดับพื้นที่ทำงาน (Workspace Rules) สำหรับ AI Agents ทุกตัวที่เข้ามาดำเนินการในระบบนี้ เพื่อสนับสนุนกระบวนการ **AISDLC (AI Software Development Life Cycle)** และรักษาความน่าเชื่อถือของคลังความรู้ **Second Brain**

---

## 🔄 1. กฎการพัฒนาร่วมกันตามกระบวนการ AISDLC

กระบวนการพัฒนาซอฟต์แวร์ใน Workspace นี้แบ่งออกเป็น 3 เฟสหลัก ซึ่งดำเนินตามลำดับขั้นตอนและเชื่อมโยงกันด้วยเอกสารเสมอ โดยมี `@pm-po` ทำหน้าที่เป็นผู้ประสานงานหลัก (Flat Orchestrator) ที่สั่งการและติดตามงานกับ Specialist Agents ทุกตัวโดยตรง:

```
                  ┌────────────────────── pm-po ──────────────────────┐
                  │                        │                          │
                  ▼                        ▼                          ▼
          [PHASE 1: DESIGN]      [PHASE 2: IMPLEMENTATION]    [PHASE 3: VERIFICATION]
          - sa (Spec)            - tech-lead (Plan/Review)    - qa (Test Plan)
          - solution-architect   - backend-dev (Code/Test)    - qa-automate (E2E)
            (Impact Analysis)    - frontend-dev (UI/Build)
                                 - security (Audit Report)
```

1.  **ห้ามข้ามขั้นตอนการทำงาน**: การทำงานจะต้องเริ่มจากเฟสดีไซน์เสมอ ห้ามมิให้ทีมพัฒนาลงมือเขียนโค้ดก่อนที่เอกสารสเปกระบบและผลกระทบสถาปัตยกรรมจะเสร็จสมบูรณ์
2.  **ขอบเขตข้อมูลที่ส่งต่อ**: ข้อมูลการออกแบบ โค้ด และผลลัพธ์การตรวจสอบความปลอดภัยจะต้องถูกแปลงลงในเอกสารของ Second Brain เพื่อให้ทีมงานสามารถใช้ประโยชน์และอ้างอิงได้
3.  **กลไกแก้ไขงาน (Feedback Loop)**:
    *   หาก `@security` ตรวจพบช่องโหว่ระดับ FAILED ใน `[[security_audit]]` ให้ส่งรายงานตรงไปยัง `@pm-po` เพื่อให้ PM ส่งงานกลับไปให้ทีม Dev แก้ไขจนกว่าจะผ่าน
    *   หาก `@qa` หรือ `@qa-automate` ตรวจพบ Bug ในระหว่างการทดสอบ ให้ส่ง Log บั๊กและรายงานการทดสอบที่ล้มเหลวกลับไปยัง `@pm-po` เพื่อสั่งการแก้ไขงาน

---

## 🧠 2. ข้อบังคับและมาตรฐานการใช้งาน Second Brain

เพื่อให้ระบบ "สมองส่วนที่สอง" ทำหน้าที่เป็นคลังความรู้ของโครงการได้อย่างมีเสถียรภาพสูงสุด ให้ปฏิบัติตามกฎดังต่อไปนี้:

1.  **การเขียนลิงก์แบบ Obsidian Wikilinks**:
    *   AI Agents ทุกตัวจะต้องใช้ไวยากรณ์วิกิลิงก์แบบ Obsidian `[[ชื่อไฟล์]]` หรือ `[[ชื่อไฟล์#หัวข้อ]]` ในการอ้างอิงเอกสารหรือข้อกำหนดระหว่างกันข้ามหมวดหมู่
    *   *ห้าม* ใช้วิธีระบุชื่อไฟล์แบบลอยๆ โดยไม่มีวงเล็บเหลี่ยมสองชั้น
2.  **กฎ Append-and-Review ใน Inbox**:
    *   ไฟล์ `second-brain/00-inbox/inbox_log.md` (`[[inbox_log]]`) จะถูกใช้เป็นกล่องรับงานหลัก
    *   เมื่อมีความต้องการใหม่ ให้เขียนต่อที่ **ด้านบนสุด (Top-append)** ของ LOGS เท่านั้น โดยระบุวันที่ ประเภท สถานะ และลิงก์เชื่อมโยงไปยังผลลัพธ์
    *   หลีกเลี่ยงการปล่อยให้บันทึกที่ล้าสมัยจมลงไปโดยไม่มีผู้ดูแล ให้หมั่นตรวจสอบและอัปเดตสถานะ
3.  **กระดานติดตามสถานะ (Project Board)**:
    *   ไฟล์ `second-brain/project_board.md` (`[[project_board]]`) เป็น Single Source of Truth สำหรับดูสถานะภาพรวมของโปรเจกต์
    *   `@pm-po` จะต้องอัปเดตสถานะงานในกระดานนี้ทุกครั้งที่มีการข้าม Phase (เช่น Inbox -> Phase 1 -> Phase 2 -> Phase 3 -> Done)
4.  **ความสอดคล้องของเส้นทางเอกสารหลัก**:
    *   **System Spec**: `second-brain/10-requirements-spec/system_spec.md` (`[[system_spec]]`)
    *   **Architecture Impact**: `second-brain/20-architecture/architecture_impact.md` (`[[architecture_impact]]`)
    *   **Security Audit**: `second-brain/40-security/security_audit.md` (`[[security_audit]]`)
    *   **Test Plan**: `second-brain/50-qa-testing/test_plan.md` (`[[test_plan]]`)
    *   **Test Execution Log**: `second-brain/50-qa-testing/test_execution.log` (`[[test_execution]]`)

---

## 🛡️ 3. การควบคุมคุณภาพและความปลอดภัย (Quality & Safety Gates)

1.  **บังคับตรวจเช็คสุขภาพข้อมูลด้วย Brain Linter**:
    *   ทุกครั้งที่ AI Agent ทำการปรับปรุงหรือบันทึกไฟล์เอกสารใหม่ใน `second-brain/` **จะต้องรันคำสั่งตรวจสอบความสมบูรณ์เสมอ**:
        ```bash
        python3 scripts/brain_linter.py
        ```
    *   หากผลลัพธ์พบ Broken Links หรือความขัดแย้งของข้อมูล (Contradiction) ห้ามส่งมอบงานและต้องทำการแก้ไขลิงก์และเนื้อหาทันที
2.  **การแก้ไขโค้ดของ Security Engineer**:
    *   บอท `@security` ห้ามทำการดัดแปลงหรือเขียนโค้ดระบบหลักด้วยตนเองเพื่อป้องกันปัญหาตรรกะระบบพัง (Business Logic Broken)
    *   มีหน้าที่วิเคราะห์ ตรวจหาความเสี่ยง และระบุวิธีการแก้ไข (Remediation Steps) ลงในรายงาน `[[security_audit]]` ให้ชัดเจนเพื่อให้ Dev เป็นผู้ลงมือทำ

---

## 💻 4. ข้อบังคับด้านการรันคำสั่งและตรวจสอบโค้ดจริง (Execution Constraints)

1.  **ห้ามคาดเดาผลการทำงาน**:
    *   บอท `@backend-dev`, `@frontend-dev`, `@security` และ `@qa-automate` ห้ามตอบรับว่างานเสร็จสิ้นหากยังไม่ได้ใช้เครื่องมือรันคำสั่ง (`run_command`) เพื่อทำการทดสอบ Unit Test, Build โครงการ หรือรันสคริปต์สแกนตรวจสอบการทำงานบนระบบจริง
2.  **การจัดการเมื่อพบบั๊กหรือ Error**:
    *   เมื่อพบปัญหาระหว่างทดสอบหรือรันบิลด์ล้มเหลว ให้อ่าน Log ข้อผิดพลาดใน Console อย่างละเอียด และวิเคราะห์ความสอดคล้องตามลำดับความต้องการ หากสเปกคลุมเครือให้ติดต่อสอบถาม PM ทันที

---

## 🤖 5. รายละเอียดและบทบาทการทำงานของ Agent Team (`.gemini/agents/`)

ระบบนี้ควบคุมการทำงานร่วมกันของ Agent 9 ตัวที่ถูกบันทึกคอนฟิกูเรชันไว้ในไดเรกทอรี [.gemini/agents/](file://.gemini/agents) ซึ่งจัดโครงสร้างการสั่งงานแบบ **Flat Orchestration** (ไม่มี nesting) ดังนี้:

### 1. PM/PO (`pm-po.md`)
*   **บทบาท**: ศูนย์กลางและผู้ควบคุมกระบวนการ AISDLC (Flat Orchestrator)
*   **อินพุตเริ่มต้น**: อ่านความต้องการล่าสุดจาก `[[inbox_log]]`
*   **การส่งงาน**: สั่งงานตรงไปยัง specialist agents แต่ละตัวตาม Phase (sa, solution-architect, tech-lead, backend-dev, frontend-dev, security, qa, qa-automate)
*   **ทักษะที่ใช้ (Skills)**: `using-agent-skills`, `context-engineering`, `idea-refine`, `interview-me`

### 2. System Analyst (`sa.md`)
*   **บทบาท**: วิเคราะห์และจัดทำข้อกำหนดเฉพาะของระบบ
*   **อินพุต**: บรีฟงานและ `[[inbox_log]]` จาก `@pm-po`
*   **เอาต์พุต**: เขียนสเปกลงไฟล์ `[[system_spec]]` พร้อมทำวิกิลิงก์กลับหา Inbox และรัน brain linter
*   **ทักษะที่ใช้ (Skills)**: `spec-driven-development`, `obsidian-markdown`, `documentation-and-adrs`

### 3. Solution Architect (`solution-architect.md`)
*   **บทบาท**: ออกแบบสถาปัตยกรรมและวิเคราะห์ผลกระทบ
*   **อินพุต**: อ่านจาก `[[system_spec]]` ตามคำสั่งของ `@pm-po`
*   **เอาต์พุต**: ใช้ `mcp_gitnexus_*` วิเคราะห์ผลกระทบ บันทึกลงใน `[[architecture_impact]]` และรัน brain linter
*   **ทักษะที่ใช้ (Skills)**: `api-and-interface-design`, `documentation-and-adrs`

### 4. Tech Lead (`tech-lead.md`)
*   **บทบาท**: ที่ปรึกษาเชิงเทคนิค ผู้จัดทำ Development Plan และทำ Code Review
*   **อินพุต**: อ่านจาก `[[system_spec]]` และ `[[architecture_impact]]` ตามคำสั่งของ `@pm-po`
*   **เอาต์พุต**: บันทึกแผนการพัฒนาลงใน `dev-plan.md` เพื่อให้ Dev ใช้อ้างอิง (ไม่มีการ delegate งานเอง)
*   **ทักษะที่ใช้ (Skills)**: `code-review-and-quality`, `code-simplification`, `doubt-driven-development`

### 5. Backend Developer (`backend-dev.md`)
*   **บทบาท**: เขียน APIs, จัดทำ Schema Database และรัน Unit Test ฝั่ง Backend
*   **อินพุต**: สเปกจาก `[[system_spec]]` และแผนจาก Tech Lead (ตามคำสั่งของ `@pm-po`)
*   **เอาต์พุต**: เขียนโค้ดฝั่ง Server, รัน Unit Test ให้ผ่าน, เขียน changelog entry และจด diary
*   **ทักษะที่ใช้ (Skills)**: `test-driven-development`, `incremental-implementation`, `source-driven-development`, `observability-and-instrumentation`, `code-simplification`, `debugging-and-error-recovery`

### 6. Frontend Developer (`frontend-dev.md`)
*   **บทบาท**: ออกแบบและพัฒนา UI/UX และเชื่อมต่อ API ฝั่ง Frontend
*   **อินพุต**: สเปกจาก `[[system_spec]]` และแผนจาก Tech Lead (ตามคำสั่งของ `@pm-po`)
*   **เอาต์พุต**: เขียนโค้ดฝั่ง Client, รัน build ให้ผ่าน, เขียน changelog entry และจด diary
*   **ทักษะที่ใช้ (Skills)**: `frontend-ui-engineering`, `test-driven-development`, `incremental-implementation`, `source-driven-development`, `code-simplification`, `debugging-and-error-recovery`

### 7. Security Engineer (`security.md`)
*   **บทบาท**: ตรวจสอบช่องโหว่ความปลอดภัยของโค้ดที่เพิ่ม/แก้ไข
*   **อินพุต**: สเปกจาก `[[system_spec]]` และซอร์สโค้ดปัจจุบัน (ตามคำสั่งของ `@pm-po`)
*   **เอาต์พุต**: บันทึกรายงานผลลงใน `[[security_audit]]` โดยระบุหัวไฟล์เป็น **[STATUS: PASSED]** หรือ **[STATUS: FAILED]** ส่งตรงไปยัง `@pm-po`
*   **ทักษะที่ใช้ (Skills)**: `security-and-hardening`, `doubt-driven-development`

### 8. QA Lead (`qa.md`)
*   **บทบาท**: ออกแบบ Test Scenario และวิเคราะห์รายงานการรันเทส
*   **อินพุต**: สเปกจาก `[[system_spec]]` (ตามคำสั่งของ `@pm-po`)
*   **เอาต์พุต**: เขียน Test Cases ลงใน `[[test_plan]]` เพื่อให้ PM ใช้สั่งงาน qa-automate ต่อไป
*   **ทักษะที่ใช้ (Skills)**: `test-driven-development`, `obsidian-markdown`

### 9. QA Automation Engineer (`qa-automate.md`)
*   **บทบาท**: พัฒนาและรันชุดทดสอบ E2E อัตโนมัติด้วย Playwright MCP
*   **อินพุต**: อ่านเงื่อนไขจาก `[[test_plan]]` (ตามคำสั่งของ `@pm-po`)
*   **เอาต์พุต**: ใช้ `mcp_playwright_*` และ `run_command` ทดสอบระบบจริงและบันทึกประวัติลงใน `[[test_execution]]`
*   **ทักษะที่ใช้ (Skills)**: `browser-testing-with-devtools`, `debugging-and-error-recovery`

---

## 🧠 6. Long-Term Memory (Tiered Architecture)

เพื่อประหยัด Token และป้องกัน Context Bloat ให้ AI Agents ปฏิบัติตามลำดับการอ่านดังนี้:
1. **Tier 1 (Mandatory)**: อ่าน `second-brain/00-Index.md` เสมอก่อนเริ่มงาน เพื่อดูสถานะโปรเจกต์
2. **Tier 2 (Phase-Aware)**: อ่านเฉพาะเอกสารของ Phase ที่กำลังทำงาน (เช่น ทำ Phase 2 ก็ให้อ่านเฉพาะ Spec และ Impact)
3. **Tier 3 (On-demand)**: ค้นหาเอกสารอื่นๆ หรือ Archives เฉพาะเมื่อจำเป็นด้วยเครื่องมือค้นหา

**กฎการจบเซสชัน (Session Finalization):**
- **อัปเดต 00-Index**: หากเปลี่ยน Phase สำเร็จ ต้องอัปเดต AISDLC Phase Tracker ใน `00-Index.md`
- **บันทึก Diary**: บันทึกปัญหาหรือสถานะงานค้างลงในโฟลเดอร์ `second-brain/diary/`
- **บันทึก Changelog**: หากมีการแก้โค้ด ให้สร้างบันทึกใน `second-brain/archives/changelog/` โดยใช้ Template

---

## 🏷️ 7. นโยบายการใช้เทมเพลตและแท็ก (Templates & Tagging)

AI ทุกตัวต้องปฏิบัติตามนโยบายการติดแท็กเมื่อสร้างไฟล์ใหม่ (ระบุใน YAML Frontmatter เสมอ):
- **ห้ามสร้างฟอร์แมตเอกสารมั่ว** ให้ดึงเทมเพลตจาก `second-brain/70-resources/templates/` มาใช้
- **นโยบายแท็ก**: ให้ตรวจสอบที่ `[[tagging-policy]]` (เช่น ต้องมี `#doc/spec` และ `#phase/design`)

---

## 🌐 8. LLM Wiki Operations (The Compounding Strategy)

คลังความรู้เปรียบเสมือนสมองที่เติบโตได้ AI มีหน้าที่รักษาสภาพสมองนี้ตลอดเวลา:
- **Ingest**: เมื่อได้ข้อมูลมาใหม่ หรือสร้างไฟล์ใหม่ ต้องสร้าง Wikilink เชื่อมจากหน้าเก่ามาหน้าใหม่เสมอ
- **Lint**: รัน `bash scripts/brain_linter.py` ทุกครั้งก่อนจบงาน เพื่อเช็คลิงก์เสีย

---

## 📂 9. กฎการระบุเส้นทางไฟล์ (Path Reference Constraints)

เพื่อให้โครงการสามารถทำงานร่วมกันได้หลายคน (Multi-user Collaboration) โดยไม่เกิดปัญหาลิงก์เสียหรือไฟล์หาไม่เจอ:
1. **ห้ามระบุ Absolute Path เด็ดขาด**: ห้ามใช้พาธแบบเต็มที่มีชื่อ User หรือ Directory เฉพาะเครื่อง เช่น `file:///Users/username/...` หรือ `/Users/username/...` ในเอกสารสเปก คอนฟิก หรือคู่มือใด ๆ
2. **ใช้ Relative Path หรือ Workspace-relative**:
   * สำหรับลิงก์มาตรฐานในเอกสาร ให้ระบุแบบ Relative เสมอ เช่น `../../.agents/skills/`
   * หรือใช้ `file://.agents/skills/` เพื่อให้สามารถเปิดอ่านได้ไม่ว่าจะอยู่ในเครื่องคอมพิวเตอร์ของใครก็ตาม
3. **ตรวจสอบก่อน Commit**: ตรวจทานเสมอว่าไม่มีพาธส่วนตัวของเครื่องตัวเองหลุดเข้าไปในซอร์สโค้ดและคอนฟิกูเรชันของโปรเจกต์

