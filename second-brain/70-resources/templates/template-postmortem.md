---
tags:
  - doc/postmortem
  - phase/verify
---

# 🔎 Post-Mortem: [Task Title / Feature Slug]

- **Date:** {{date}}
- **Related Task/Epic:** [[project_board]]
- **Responsible Agent:** @pm-po / @solution-architect / @backend-dev

---

## 🛑 What Went Wrong? (อาการข้อผิดพลาด)

_อธิบายปัญหา บั๊ก หรือการ Looping ของ Agent ที่เกิดขึ้นอย่างละเอียด พร้อมแนบ Error Logs หรือพฤติกรรมที่ไม่ถูกต้อง (ถ้ามี)_

-

## 🔍 Root Cause Analysis (สาเหตุหลัก)

_อธิบายเหตุผลทางเทคนิค หรือความเข้าใจที่คลาดเคลื่อนของ Agent ที่ทำให้เกิดปัญหานี้_

-

## 🛠️ How We Fixed It (วิธีการแก้ไขที่ถูกต้อง)

_อธิบายวิธีแก้ปัญหา พร้อมโค้ดตัวอย่างที่ทำงานได้ถูกต้อง หรือแนวคิดทางสถาปัตยกรรมที่ใช้แก้_

-

## 🧠 Distilled Rule for Future Reference (กฎที่สรุปได้สำหรับงานถัดไป)

> [!IMPORTANT]
> **Anti-Pattern Rule:** [เขียนกฎ 1 ประโยคสั้นๆ เพื่อนำไปอัปเดตลงใน AGENTS.md หรือ lessons_learned.md เช่น "ห้ามใช้... เมื่อเกิด..."]

## 🔄 Rule Compounding Trigger

_(ประเมินว่าข้อผิดพลาดนี้ เป็นปัญหาเรื้อรังที่เกิดซ้ำซากเกิน 1 ครั้งหรือไม่?)_

- [ ] **NO:** เป็นปัญหาเฉพาะเคส ให้จบแค่การบันทึกลง `[[lessons_learned]]`
- [ ] **YES:** เป็นปัญหาซ้ำซาก (Anti-pattern เดิม)
  - **Action Required:** ต้องนำกฎด้านบนไปอัปเดตเพิ่มในหัวข้อ `Never Do` ของบอทที่เกี่ยวข้องในไฟล์ `AGENTS.md` หรือไฟล์คอนฟิกของบอทนั้นๆ ทันที
