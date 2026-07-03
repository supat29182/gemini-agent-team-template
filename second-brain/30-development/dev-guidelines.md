---
date: 2026-06-23
author: backend-dev
tags:
  - doc/kb
  - phase/implement
---

# 💻 Development Guidelines

> คู่มือและข้อตกลงสำหรับทีมพัฒนาในโปรเจกต์ AISDLC

## Coding Conventions

### ทั่วไป

- ใช้ **Meaningful Variable Names** — ห้ามตั้งชื่อตัวแปรว่า `x`, `temp`, `data` โดยไม่มีบริบท
- ใช้ **camelCase** สำหรับ JavaScript/TypeScript, **snake_case** สำหรับ Python
- ทุกฟังก์ชันที่เป็น Public API ต้องมี JSDoc/Docstring
- ห้าม commit โค้ดที่มี `console.log` หรือ `print` ที่ใช้ debug ทิ้งไว้

### Error Handling

- ห้ามใช้ empty catch blocks — ต้อง log error หรือ throw ต่อเสมอ
- ใช้ custom error types สำหรับ business logic errors

### Git Commit Messages

- ใช้ format: `type(scope): description` เช่น `feat(api): add line notify endpoint`
- Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`

## API Contracts

- ทุก endpoint ต้องตอบกลับในรูปแบบ JSON มาตรฐาน:
  ```json
  {
    "success": true,
    "data": {},
    "error": null
  }
  ```
- HTTP Status Codes: `200` OK, `201` Created, `400` Bad Request, `401` Unauthorized, `404` Not Found, `500` Server Error
- ทุก request ที่รับ user input ต้องมี input validation

## Database Migration

- ทุกครั้งที่แก้ไข Schema ต้องสร้าง migration file
- ห้ามแก้ไข migration ที่ถูก apply ไปแล้ว — ให้สร้าง migration ใหม่เสมอ

## อ้างอิง

- ข้อกำหนดระบบ: `[[system_spec]]`
- ผลกระทบสถาปัตยกรรม: `[[architecture_impact]]`
