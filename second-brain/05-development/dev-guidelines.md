---
date: 2026-06-23
author: backend-dev
tags:
  - doc/kb
  - phase/implement
---

# 💻 Development Guidelines

> Manual and agreements for the development team in the AISDLC project

## Coding Conventions

### General

- Use **Meaningful Variable Names** — Do not name variables `x`, `temp`, `data` without proper context.
- Use **camelCase** for JavaScript/TypeScript, and **snake_case** for Python.
- All public API functions must include JSDoc/Docstring.
- Do not commit code containing debug statements like `console.log` or `print`.

### Error Handling

- Do not use empty catch blocks — always log the error or rethrow it.
- Use custom error types for business logic errors.

### Git Commit Messages

- Use format: `type(scope): description` e.g., `feat(api): add line notify endpoint`
- Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`

## API Contracts

- All endpoints must respond with the standard JSON format:
  ```json
  {
    "success": true,
    "data": {},
    "error": null
  }
  ```
- HTTP Status Codes: `200` OK, `201` Created, `400` Bad Request, `401` Unauthorized, `404` Not Found, `500` Server Error
- All requests receiving user input must have input validation.

## Database Migration

- A migration file must be created every time the Database Schema is modified.
- Never edit already-applied migrations — always create a new migration.

## References

- System Specification: `[[system_spec]]`
- Architecture Impact: `[[architecture_impact]]`
