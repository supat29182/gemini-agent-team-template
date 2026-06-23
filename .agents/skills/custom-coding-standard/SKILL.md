---
name: custom-coding-standard
description: แม่แบบและแนวทางปฏิบัติสำหรับการกำหนดมาตรฐานการเขียนโค้ดและโครงสร้างของโปรเจกต์
---

# Custom Coding Standard & Architecture Guidelines

คู่มือนี้สำหรับระบุรูปแบบโค้ด (Coding Conventions) และรูปแบบโครงสร้างไฟล์ของระบบ โดยทีมพัฒนาสามารถกำหนดหรือแก้ไขคู่มือนี้ เพื่อให้บอทผู้พัฒนา (`backend-dev` และ `frontend-dev`) เขียนโค้ดเป็นไปในแนวทางเดียวกันทั้งองค์กร

## 1. การกำหนดโครงสร้างโปรเจกต์ (Project Directory Structure)
ระบุรายละเอียดโครงสร้างโฟลเดอร์ของซอร์สโค้ดหลัก เช่น:
- `/src/components`: สำหรับ UI Components
- `/src/services`: สำหรับ API Service calls
- `/src/utils`: สำหรับ Helper functions ต่างๆ

## 2. กฎการตั้งชื่อและการจัดรูปแบบ (Naming Conventions)
ระบุรูปแบบที่ต้องการให้แน่ชัด:
- **ตัวแปรและฟังก์ชัน**: แนะนำให้ใช้ `camelCase` (เช่น `getUserProfile`)
- **ชื่อคลาสหรือโมดูล**: แนะนำให้ใช้ `PascalCase` (เช่น `UserProfileCard`)
- **ชื่อไฟล์**: แนะนำให้ใช้ `kebab-case` (เช่น `user-profile.js`)
- **ค่าคงที่ (Constants)**: แนะนำให้ใช้ `UPPER_SNAKE_CASE` (เช่น `MAX_RETRY_COUNT`)

## 3. รูปแบบการจัดการข้อผิดพลาด (Error Handling Pattern)
- ทุก API call หรือการเชื่อมต่อฐานข้อมูล จะต้องมี Block `try-catch` เสมอ
- หากเกิด Error ให้ทำการ Log ด้วยระดับความรุนแรง (Log Levels) ที่ถูกต้องผ่านระบบ logging กลางของระบบ และส่ง response error ในรูปแบบมาตรฐาน:
  ```json
  {
    "success": false,
    "error": "Error message details"
  }
  ```

## 4. มาตรฐานความปลอดภัยของซอร์สโค้ด (Security Coding Guidelines)
- ห้ามใส่ API Key, Secret Token หรือ Credentials ใดๆ ไว้ในซอร์สโค้ด (Hardcoded Secrets) โดยเด็ดขาด ให้ใช้ `.env` หรือ configuration files
- ข้อมูล Input ที่รับมาจาก Client จะต้องถูกทำการ Validate และ Sanitize เสมอเพื่อป้องกัน XSS และ SQL Injection
