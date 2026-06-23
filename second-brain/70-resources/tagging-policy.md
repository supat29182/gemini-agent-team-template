# 🏷️ นโยบายการติดแท็ก (Tagging Policy)

เพื่อให้คลังความรู้ Second Brain เป็นระเบียบและค้นหาง่าย AI Agents ทุกตัวต้องปฏิบัติตามมาตรฐานการติดแท็กใน Frontmatter ของไฟล์ดังนี้:

### กฎสำคัญ:
- **ใช้ Nested Tags เท่านั้น** — รูปแบบ `หมวดหมู่/หมวดหมู่ย่อย`
- **ทุกไฟล์เอกสารต้องมี `#doc/*` อย่างน้อย 1 แท็ก**
- **แท็กต้องเป็นตัวพิมพ์เล็ก (lowercase) ทั้งหมด**

### แท็กมาตรฐานที่อนุญาต:

```text
# Document Type (ประเภทเอกสาร)
doc/index        doc/adr         doc/changelog  
doc/kb           doc/diary       doc/snapshot   
doc/spec         doc/eval        doc/postmortem
doc/architecture doc/brd         doc/user-story
doc/dev-plan

# AISDLC Phase (ช่วงเวลาของโครงการ)
phase/inbox      phase/design    phase/implement   
phase/verify     phase/ship      phase/initiation
phase/implementation
```
