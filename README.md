# 🚀 Gemini Agent Team Template

ยินดีต้อนรับสู่โปรเจกต์ **Gemini Agent Team Template**! 
โปรเจกต์นี้คือแม่แบบสำหรับทีมพัฒนาซอฟต์แวร์เสมือนจริง (AI Agent Team) ที่ขับเคลื่อนด้วยสถาปัตยกรรม **Event-Driven Orchestration** ควบคู่ไปกับการออกแบบ **Token Optimization** ผ่านเครื่องมือวิเคราะห์โค้ดอัจฉริยะอย่าง `GitNexus`

ทีม Agent ของเราประกอบไปด้วยบทบาทต่างๆ ที่ครอบคลุมตั้งแต่การเก็บ Requirement, การออกแบบระบบ (System Design), การเขียนโค้ดทั้งหน้าบ้านและหลังบ้าน, ไปจนถึงการเขียนสคริปต์ทดสอบระบบอัตโนมัติ (Automated E2E Testing)

---

## 🏗️ สถาปัตยกรรมของ AgentFlow

ระบบได้ถูกออกแบบให้ทำงานแบบผสมผสานทั้ง **Sequential (ทำทีละขั้น)** และ **Parallel (ทำคู่ขนาน)** เพื่อความรวดเร็วและประหยัด Token

### 📊 1. Flowchart ภาพรวมของระบบ

```mermaid
graph TD
    INBOX["inbox_log.md"] -->|"1. PM อ่าน Requirement"| PM(("pm-po"))
    PM -->|"Phase 1: Design"| SA("sa")
    SA -->|"Draft Spec & API"| ARCH("solution-architect")
    ARCH -->|"Impact Analysis"| PM
    
    PM -->|"Phase 2: Sync Point 2"| BACK("backend-dev")
    PM -->|"Phase 2: Sync Point 2"| QA_P("qa-automate (Test Plan)")
    BACK -.->|"เสร็จ 2 ตัว"| FRONT("frontend-dev")
    QA_P -.->|"เสร็จ 2 ตัว"| FRONT
    FRONT -->|"Phase 2: Sync Point 2.5"| PM
    
    PM -->|"Phase 3: Sync Point 3"| SEC("security (Audit)")
    PM -->|"Phase 3: Sync Point 3"| QA_E("qa-automate (Execution)")
    
    SEC -.->|"Failed"| BACK
    QA_E -.->|"Failed"| FRONT
    
    SEC -.->|"Passed"| DONE["Project Board: DONE"]
    QA_E -.->|"Passed"| DONE
```

### ⏱️ 2. Sequence Diagram (เจาะลึกเมื่อสั่งงาน)

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant PM as pm-po
    participant SA as sa
    participant Arch as solution-architect
    participant Devs as backend and frontend
    participant QA as qa-automate
    participant Nexus as GitNexus
    
    User->>PM: โยน Requirement (ลง Inbox)
    Note over PM: PM ห้ามอ่านโค้ดเองเด็ดขาด
    
    rect rgb(240, 248, 255)
        Note right of PM: PHASE 1: DESIGN
        PM->>SA: สร้าง System Spec
        SA-->>PM: เสร็จสิ้น (system_spec.md)
        PM->>Arch: วิเคราะห์ Impact
        Arch->>Nexus: mcp_gitnexus_impact
        Nexus-->>Arch: ส่ง JSON สรุปกลับมา
        Arch-->>PM: เสร็จสิ้น (architecture_impact.md)
    end

    rect rgb(240, 255, 240)
        Note right of PM: PHASE 2: IMPLEMENTATION (Event-Driven)
        PM->>Devs: สั่งรัน backend-dev
        PM->>QA: สั่งรัน qa-automate (ทำ Test Plan)
        Note over PM: PM เข้าโหมด Sleep
        
        Devs->>Nexus: ค้นหาโครงสร้างเก่า
        Devs-->>PM: ปลุก PM (Backend เสร็จ)
        QA-->>PM: ปลุก PM (Test Plan เสร็จ)
        
        PM->>Devs: สั่งรัน frontend-dev
        Devs-->>PM: ปลุก PM (Frontend เสร็จ)
    end

    rect rgb(255, 240, 245)
        Note right of PM: PHASE 3: VERIFICATION
        PM->>QA: สั่งรัน qa-automate (รัน E2E Test)
        PM->>Devs: สั่งรัน security
        Note over PM: PM เข้าโหมด Sleep
        
        QA-->>PM: ปลุก PM (เจอ Error ตัด log สั้นๆ 50 บรรทัด)
        Note over PM: Feedback Loop: ตีกลับงานให้ Dev
        PM->>Devs: นำ Log 50 บรรทัดส่งให้แก้
    end
    
    PM->>User: อัปเดตบอร์ด สรุปงานส่งมอบ
```

---

## 📝 กระบวนการทำงานแบบ Step-by-Step

**จุดเริ่มต้น:**
ผู้ใช้งานโยน Requirement ลงมาในแชท บอทตัวแรกที่ตื่นขึ้นมาคือ **`@pm-po`** (Project Manager) ทำหน้าที่รับ Requirement บันทึกลงใน `inbox_log.md` 

**Phase 1: Design (ขั้นตอนการออกแบบ)**
1. `pm-po` สั่งงานให้ **`@sa` (System Analyst)** ทำการวิเคราะห์ Requirement และเขียนเอกสาร `system_spec.md` และ `api_contract.yaml`
2. `pm-po` ส่งไม้ต่อให้ **`@solution-architect`** ตรวจสอบผลกระทบกับโครงสร้างเดิม (Blast Radius) โดยอาศัยเครื่องมือ `GitNexus` เพื่อไม่ต้องดึงโค้ดทั้งหมดมาอ่านให้เปลือง Token

**Phase 2: Implementation (ขั้นตอนการสร้าง)**
1. `pm-po` สั่งรัน **`@backend-dev`** และ **`@qa-automate`** ให้ทำงานพร้อมกัน 
2. **`@backend-dev`** พัฒนา API และฐานข้อมูล ส่วน **`@qa-automate`** จะสร้าง `test_plan.md` ล่วงหน้า (Shift-Left Testing)
3. ระหว่างนี้ `pm-po` จะ "หลับ" เพื่อหยุดกิน Token จนกว่าบอททั้ง 2 ตัวจะทำงานเสร็จ (อัปเดตไฟล์ `task_locks.json` สำเร็จ)
4. เมื่อตื่นขึ้นมา `pm-po` จะสั่งรัน **`@frontend-dev`** ให้นำ API ไปต่อเข้ากับ User Interface

**Phase 3: Verification (ขั้นตอนการตรวจสอบ)**
1. เมื่อ Frontend เสร็จ `pm-po` จะสั่งรัน **`@security`** ตรวจสอบช่องโหว่ความปลอดภัย และ **`@qa-automate`** รัน E2E Test บนเบราว์เซอร์จริงด้วย `Playwright MCP`
2. หากทดสอบไม่ผ่าน (มีบั๊ก) QA จะส่ง Error Log สั้นๆ ตัดมาไม่เกิน 50 บรรทัด (Log Truncation) เพื่อประหยัด Token และให้ `pm-po` ตีกลับไปให้ Dev แก้ไข
3. เมื่อทุกอย่างผ่านฉลุย `pm-po` จะแจ้งเตือนผู้ใช้ว่าฟีเจอร์เสร็จสมบูรณ์

---

## 🎭 จำลองเหตุการณ์ที่มีโอกาสเกิดขึ้น (Edge Case Simulations)

เพื่อให้เห็นภาพการทำงานจริง นี่คือสถานการณ์จำลองและปฏิกิริยาของระบบ:

### 🚨 1. ลูกค้าให้ Requirement มาแบบคลุมเครือ
- **สถานการณ์:** ผู้ใช้พิมพ์ใน Inbox แค่ว่า *"อยากได้ปุ่มกดแชร์"*
- **การตอบสนอง:** `@pm-po` จะใช้สกิลสัมภาษณ์เพื่อหยุดการสั่งงานและถามคำถามกับผู้ใช้ทีละ 1 คำถาม จนกว่าสเปกจะชัดเจน จึงจะส่งต่อให้ `@sa`

### 🚨 2. Frontend จินตนาการ API เอง (Hallucination)
- **สถานการณ์:** `@backend-dev` ยังพัฒนาไม่เสร็จ แต่ `@frontend-dev` เริ่มมั่วโครงสร้าง Mock Data ขึ้นมาเอง
- **การตอบสนอง:** กฎ API Contract จะทำงาน บอท Frontend จะถูกบังคับให้อ่าน `api_contract.yaml` ก่อนเขียนโค้ดเสมอ หากไม่มีข้อมูลในนั้น บอทจะหยุดรอ

### 🚨 3. ระบบเทสพังและโดนตีกลับ (The Feedback Loop)
- **สถานการณ์:** บอท `@qa-automate` รัน E2E แล้วพัง (Error 500)
- **การตอบสนอง:** QA จะบันทึก Log ลงในไฟล์แบบตัดทอนไม่เกิน 50 บรรทัด (Log Truncation) แล้วส่งให้ `@pm-po` ตีกลับงานให้ `@backend-dev` ซ่อม โดย Dev ต้องรัน `mcp_gitnexus_impact` วิเคราะห์ผลกระทบก่อนแก้โค้ด

### 🚨 4. นักพัฒนาแก้บั๊กไม่สำเร็จจนติดลูป (Deadlock Prevention)
- **สถานการณ์:** สืบเนื่องจากเหตุการณ์ก่อนหน้า บั๊กแก้ยาก `@backend-dev` พยายามแก้และรันเทสพังซ้ำหลายรอบ
- **การตอบสนอง:** เมื่อล้มเหลวติดต่อกันครบ 3 ครั้ง บอทจะยอมแพ้ เปลี่ยนสถานะล็อกเป็น `failed` แล้วเรียกให้มนุษย์เข้ามาดู เพื่อป้องกันระบบค้าง (Infinite Wait) และป้องกันกิน Token ฟรี

### 🚨 5. ตรวจพบช่องโหว่ความปลอดภัยร้ายแรง
- **สถานการณ์:** `@security` ตรวจพบ Hardcoded Secret ในโค้ด Frontend
- **การตอบสนอง:** บอท Security จะไม่แก้โค้ดเอง (กันตรรกะระบบพัง) แต่มันจะทำรายงานลง `security_audit.md` (สถานะ FAILED) แจ้ง PM ให้ตีกลับงานไปที่ Frontend เพื่อแก้ปัญหา

---

## 🛠️ วิธีการใช้งาน Repository นี้ (How to use)

### 1. โครงสร้างของ Project 
โปรเจกต์นี้ทำงานร่วมกับโครงสร้าง Agent ที่ฝังอยู่ในโฟลเดอร์ `.agents/`:
- `.agents/AGENTS.md` - รัฐธรรมนูญของ AI กำหนดกฎกติกาการทำงานทั้งหมด (เช่น การใช้ GitNexus, กฎของ PM)
- `.agents/agents/` - ไฟล์บุคลิกภาพ (System Prompt) ของบอทแต่ละตัว
- `second-brain/` - โฟลเดอร์สมองที่ 2 สำหรับเก็บเอกสาร สเปก โค้ด และบันทึกสถานะโปรเจกต์ (`task_locks.json`)

### 2. การเรียกใช้งานฟีเจอร์ใหม่
เมื่อคุณมีไอเดียหรือฟีเจอร์ที่อยากให้ AI ทีมนี้พัฒนา คุณไม่จำเป็นต้องไปคุยกับ Dev หรือ QA ด้วยตัวเอง! ให้คุณพิมพ์คำสั่งในแชทถึง **PM** ได้เลย เช่น:
> *"ช่วยทำระบบ Login Authentication ด้วย JWT ให้หน่อย"*

**PM (`@pm-po`)** จะตื่นขึ้นมา สร้างโฟลเดอร์ใน `second-brain` แจกแจงงานลง `project_board.md` และปลุกบอทตัวอื่นๆ ให้ทำงานตาม Flow ด้านบนให้คุณโดยอัตโนมัติ 

### 3. ส่วนเสริมที่จำเป็น (MCP Servers)
เพื่อให้ Agent ทำงานได้อย่างเต็มประสิทธิภาพ โปรเจกต์นี้จะพึ่งพาเครื่องมือ (Tools) เบื้องหลัง:
- **`GitNexus`**: สำหรับให้ Librarian, Dev, และ Architect สร้าง Call Graph ของโปรเจกต์ ช่วยประหยัด Token การอ่านไฟล์โค้ด
- **`Playwright`**: สำหรับให้ QA Automate เปิดเบราว์เซอร์แล้วคลิกทดสอบหน้าเว็บจริงๆ 

*(ระบบจะรัน MCP พวกนี้ผ่าน `npx` อัตโนมัติในเบื้องหลังตามคิวที่เรียกใช้งาน)*
