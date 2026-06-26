---
date: 2026-06-23
author: pm-po
tags:
  - doc/kb
  - phase/ship
---

# 🚀 Deployment & Delivery Playbook

> คู่มือการเตรียมระบบสำหรับการนำส่ง (Deployment) และ Release

## Pre-Deploy Checklist

- [ ] ผ่าน Security Audit (`[[security_audit]]` = `[STATUS: PASSED]`)
- [ ] ผ่าน E2E Testing (`[[test_execution]]` = All Passed)
- [ ] อัปเดต Changelog ล่าสุดใน `second-brain/archives/changelog/`
- [ ] อัปเดต `[[project_board]]` เป็น `Done`
- [ ] Review โค้ดโดย Tech Lead เรียบร้อย

## Deployment Steps

1. **Build Production Bundle**

   ```bash
   npm run build
   ```

2. **Run Final Smoke Test**

   ```bash
   npm run test:e2e -- --headed
   ```

3. **Deploy to Staging**
   - (ระบุขั้นตอนการ deploy ตาม infrastructure ของโปรเจกต์)

4. **Verify on Staging**
   - ตรวจสอบ core features ทำงานถูกต้อง
   - ตรวจสอบ logs ไม่มี error

5. **Deploy to Production**
   - (ระบุขั้นตอนการ deploy production)

## Rollback Plan

- หากพบปัญหาหลัง deploy ให้ revert ไปยัง version ก่อนหน้า
- บันทึก Post-Mortem ลงใน `second-brain/60-delivery-ops/postmortem/`

## อ้างอิง

- Security Audit: `[[security_audit]]`
- Test Results: `[[test_execution]]`
- Project Board: `[[project_board]]`
