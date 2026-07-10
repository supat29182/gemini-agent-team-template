---
date: 2026-06-23
author: pm-po
tags:
  - doc/kb
  - phase/ship
---

# 🚀 Deployment & Delivery Playbook

> Manual for deployment preparation and releases

## Pre-Deploy Checklist

- [ ] Security Audit passed (`[[security_audit]]` = `[STATUS: PASSED]`)
- [ ] E2E Testing passed (`[[test_execution]]` = All Passed)
- [ ] Latest Changelog updated in `second-brain/archives/changelog/`
- [ ] `[[project_board]]` updated to `Done`
- [ ] Security Audit passed and code reviewed successfully

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
   - (Specify the deploy steps based on the project's infrastructure)

4. **Verify on Staging**
   - Verify that core features work correctly
   - Verify that logs have no errors

5. **Deploy to Production**
   - (Specify the production deploy steps)

## Rollback Plan

- If issues are found after deploy, revert to the previous version immediately.
- Record the Post-Mortem in `second-brain/60-delivery-ops/postmortem/`

## References

- Security Audit: `[[security_audit]]`
- Test Results: `[[test_execution]]`
- Project Board: `[[project_board]]`
