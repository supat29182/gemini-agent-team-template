# 🧠 00-Index (Master Hub)

> [!IMPORTANT]
> หน้านี้คือจุดเริ่มต้นและ **Single Source of Truth** สำหรับ AI Assistants ทุกตัวในโปรเจกต์นี้
> **AI ทุกตัวต้องตรวจสอบไฟล์นี้ก่อนเริ่มทำงานเสมอ** เพื่อเช็คสถานะปัจจุบันของโปรเจกต์และติดตาม AISDLC Phase

---

## 🎯 AISDLC Phase Tracker

| สถานะปัจจุบัน (Current Phase)         | ไฟล์ที่เกี่ยวข้องหลัก                                                                                         |
| :------------------------------------ | :------------------------------------------------------------------------------------------------------------ |
| [ ] Inbox/Initiation                   | [[inbox_log]], [[project_board]]                                                                              |
| [ ] Phase 1: Design                    | [[system_spec]], [[architecture_impact]]                                                                      |
| [ ] Phase 2: Implementation            | Source Code, [[security_audit]]                                                                               |
| [ ] Phase 3: Verification              | [[test_plan]], [[test_execution]]                                                                             |
| [ ] Phase 4: Post-Mortem & Reflection | [[lessons_learned]], [[template-postmortem]]                                                                  |

_เมื่อจบแต่ละ Phase, ให้ AI หรือ PM/PO อัปเดตเครื่องหมายถูก `[x]` ที่นี่และเลื่อนสถานะไป Phase ถัดไป_

---

## 📂 สารบัญโครงการ (Project Directory)

- **📥 00-Inbox**: กล่องรับงานดิบและการประเมินเริ่มต้น ➔ [[inbox_log]]
- **📊 01-Project Board**: กระดานสถานะงาน (Kanban) ➔ [[project_board]]
- **🧠 05-Knowledge Base**: คลังความรู้สะสมและบทเรียน ➔ [[lessons_learned]]
- **📝 10-Requirements**: เอกสารระบบและ User Journey ➔ [[system_spec]]
- **📐 20-Architecture**: การออกแบบและประเมินผลกระทบ ➔ [[architecture_impact]]
- **💻 30-Development**: พื้นที่ของนักพัฒนาและกฎการเขียนโค้ด ➔ [[dev-guidelines]]
- **🛡️ 40-Security**: รายงานการออดิตและ OWASP ➔ [[security_audit]]
- **🧪 50-QA**: แผนการทดสอบและผลลัพธ์ ➔ [[test_plan]], [[test_execution]]
- **🚀 60-Delivery**: การเตรียมปล่อยสู่ Production ➔ [[deployment-playbook]]
- **📚 70-Resources**: คู่มือ, Templates, และนโยบาย ➔ [[tagging-policy]]
- **📓 Diary**: บันทึกย่อการทำงานของ AI ➔ `second-brain/diary/`
- **🗄️ Archives**: เก็บประวัติและ Changelog เก่า ➔ `second-brain/archives/changelog/`

---

## ⚙️ กฎเหล็กประจำโปรเจกต์ (Quick Rules)

1. **อ่าน 00-Index เสมอ**
2. **ใช้ `[[wikilinks]]` ในการอ้างอิงทุกครั้ง**
3. **ห้ามแก้ไขโค้ดโดยพลการ หากยังไม่ได้อัปเดต Spec**
4. **บันทึกประวัติการสะท้อนคิดลงใน Post-Mortem เมื่อมีข้อผิดพลาดหรือเมื่อสิ้นสุดงาน**
5. **บันทึก Diary ทุกท้ายเซสชันการทำงาน** (ถ้ามีการแก้ไขสำคัญ)

ดูรายละเอียดกฎทั้งหมดได้ที่ [[AGENTS]] หรือไฟล์ `.agents/AGENTS.md`
