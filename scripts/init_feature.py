#!/usr/bin/env python3
import os
import sys
import argparse
import datetime
import json

def main():
    parser = argparse.ArgumentParser(description="Initialize a new feature directory and templates for Strategy B")
    parser.add_argument("--slug", required=True, help="Folder slug for the feature (e.g. line-notify)")
    parser.add_argument("--title", help="Title of the feature/CR (e.g. Line Notify System)")
    parser.add_argument("--type", choices=["feature", "cr", "bug"], default="feature", help="Type of task (feature, cr, bug)")
    args = parser.parse_args()

    slug = args.slug.strip().lower().replace(" ", "-")
    
    # Ensure slug format matches the type
    if args.type == "cr" and not slug.startswith("cr-"):
        slug = f"cr-{slug}"
    elif args.type == "bug" and not slug.startswith("bug-"):
        slug = f"bug-{slug}"

    title = args.title.strip() if args.title else slug.replace("-", " ").title()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_dir = os.path.abspath(os.path.join(script_dir, ".."))
    
    current_date = datetime.date.today().strftime("%Y-%m-%d")

    # Define paths
    folder_type = "features"
    if args.type == "cr":
        folder_type = "cr"
    elif args.type == "bug":
        folder_type = "bug"

    phases = {
        "requirements": f"second-brain/10-requirements-spec/{folder_type}/{slug}",
        "architecture": f"second-brain/20-architecture/{folder_type}/{slug}",
        "development": f"second-brain/30-development/{folder_type}/{slug}",
        "security": f"second-brain/40-security/{folder_type}/{slug}",
        "qa": f"second-brain/50-qa-testing/{folder_type}/{slug}"
    }

    print(f"Creating directories for '{slug}' ({args.type}) in '{folder_type}'...")
    for phase_name, rel_path in phases.items():
        abs_path = os.path.join(workspace_dir, rel_path)
        os.makedirs(abs_path, exist_ok=True)
        # Create a .gitkeep to ensure the directory is tracked by git
        gitkeep_path = os.path.join(abs_path, ".gitkeep")
        if not os.path.exists(gitkeep_path):
            with open(gitkeep_path, 'w') as f:
                pass
        print(f"  [Created] {rel_path}")

    # Copy templates
    templates = []
    if args.type in ["feature", "cr"]:
        templates = [
            ("second-brain/70-resources/templates/template-brd.md", f"{phases['requirements']}/brd.md", "sa"),
            ("second-brain/70-resources/templates/template-epics-user-stories.md", f"{phases['requirements']}/epics_user_stories.md", "sa"),
            ("second-brain/70-resources/templates/template-system-spec.md", f"{phases['requirements']}/system_spec.md", "sa")
        ]

    print("\nCopying templates and filling placeholders...")
    for template_rel, target_rel, author in templates:
        template_path = os.path.join(workspace_dir, template_rel)
        target_path = os.path.join(workspace_dir, target_rel)

        if not os.path.exists(template_path):
            print(f"  [Warning] Template {template_rel} not found. Skipping.")
            continue

        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Replace placeholders
            content = content.replace("YYYY-MM-DD", current_date)
            content = content.replace("[Task/Feature Name]", title)
            content = content.replace("[ชื่องาน/ฟีเจอร์]", title)
            content = content.replace("[Task Name]", title)
            content = content.replace("[ชื่องาน]", title)

            # Write target file
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  [Created File] {target_rel}")
        except Exception as e:
            print(f"  [Error] Failed to create {target_rel}: {e}")

    # Generate decentralized lock files
    locks_dir = os.path.join(workspace_dir, phases['development'], "locks")
    os.makedirs(locks_dir, exist_ok=True)
    print(f"\nInitializing decentralized lock files in '{phases['development']}/locks'...")

    lock_definitions = {
        "ux-ui": {"status": "idle", "locked_by": "", "locked_at": "", "completed_at": "", "ttl_mins": 40},
        "backend-dev": {"status": "idle", "locked_by": "", "locked_at": "", "completed_at": "", "ttl_mins": 45},
        "frontend-dev": {"status": "idle", "locked_by": "", "locked_at": "", "completed_at": "", "ttl_mins": 45},
        "qa-test-plan": {"status": "idle", "locked_by": "", "locked_at": "", "completed_at": "", "ttl_mins": 35},
        "security-audit": {"status": "idle", "locked_by": "", "locked_at": "", "completed_at": "", "ttl_mins": 25},
        "qa-automate-execution": {"status": "idle", "locked_by": "", "locked_at": "", "completed_at": "", "ttl_mins": 35}
    }

    # Customize locks for bug fixes
    if args.type == "bug":
        lock_definitions["qa-test-plan"]["status"] = "skipped"
        lock_definitions["qa-test-plan"]["reason"] = "Bug fix - No new test plan required"
        lock_definitions["security-audit"]["status"] = "skipped"
        lock_definitions["security-audit"]["reason"] = "Bug fix - No new API endpoints, regression check only"

    for agent_name, init_data in lock_definitions.items():
        lock_file_path = os.path.join(locks_dir, f"{agent_name}.json")
        try:
            with open(lock_file_path, 'w', encoding='utf-8') as f:
                json.dump(init_data, f, indent=2, ensure_ascii=False)
            print(f"  [Created Lock File] {phases['development']}/locks/{agent_name}.json")
        except Exception as e:
            print(f"  [Error] Failed to create lock file for {agent_name}: {e}")

    # For bugs, create a diagnosis document directly
    if args.type == "bug":
        diagnosis_rel = f"{phases['architecture']}/bug_diagnosis.md"
        diagnosis_path = os.path.join(workspace_dir, diagnosis_rel)
        diagnosis_content = f"""---
date: {current_date}
author: architect
tags:
  - doc/architecture
  - phase/design
---

# 🐛 Bug Diagnosis & Root Cause Analysis: {title}

- **Date:** {current_date}
- **Feature/Context:** {slug}
- **Status:** Investigating

## 1. Steps to Reproduce
(Explain steps to reproduce)

## 2. Root Cause Analysis
(Analyze root cause and impact on the existing system)

## 3. Proposed Fix
(Proposed code fix)
"""
        try:
            with open(diagnosis_path, 'w', encoding='utf-8') as f:
                f.write(diagnosis_content)
            print(f"  [Created File] {diagnosis_rel}")
        except Exception as e:
            print(f"  [Error] Failed to create {diagnosis_rel}: {e}")

    # Register to project board automatically
    print("\nRegistering task on the project board...")
    try:
        import subprocess
        cmd = [
            sys.executable,
            os.path.join(script_dir, "project_board_manager.py"),
            "--action", "add",
            "--slug", slug,
            "--title", title,
            "--type", args.type
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"  [Board Manager] {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"  [Error] Failed to register to project board: {e.stderr.strip()}")
    except Exception as e:
        print(f"  [Error] Failed to register to project board: {e}")

    print("\nDone!")

if __name__ == "__main__":
    main()
