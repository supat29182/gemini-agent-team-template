#!/usr/bin/env python3
import os
import sys
import argparse
import datetime

def main():
    parser = argparse.ArgumentParser(description="Initialize a new feature directory and templates for Strategy B")
    parser.add_argument("--slug", required=True, help="Folder slug for the feature (e.g. line-notify)")
    parser.add_argument("--title", help="Title of the feature/CR (e.g. Line Notify System)")
    args = parser.parse_args()

    slug = args.slug.strip().lower().replace(" ", "-")
    title = args.title.strip() if args.title else slug.replace("-", " ").title()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_dir = os.path.abspath(os.path.join(script_dir, ".."))
    
    current_date = datetime.date.today().strftime("%Y-%m-%d")

    # Define paths
    phases = {
        "requirements": f"second-brain/10-requirements-spec/features/{slug}",
        "architecture": f"second-brain/20-architecture/features/{slug}",
        "development": f"second-brain/30-development/features/{slug}",
        "security": f"second-brain/40-security/features/{slug}",
        "qa": f"second-brain/50-qa-testing/features/{slug}"
    }

    print(f"Creating directories for feature slug '{slug}'...")
    for phase_name, rel_path in phases.items():
        abs_path = os.path.join(workspace_dir, rel_path)
        os.makedirs(abs_path, exist_ok=True)
        print(f"  [Created] {rel_path}")

    # Copy templates
    templates = [
        ("second-brain/70-resources/templates/template-brd.md", f"{phases['requirements']}/brd.md", "pm-po"),
        ("second-brain/70-resources/templates/template-epics-user-stories.md", f"{phases['requirements']}/epics_user_stories.md", "pm-po"),
        ("second-brain/70-resources/templates/template-system-spec.md", f"{phases['requirements']}/system_spec.md", "sa"),
        ("second-brain/70-resources/templates/template-dev-plan.md", f"{phases['development']}/dev-plan.md", "tech-lead"),
        ("second-brain/70-resources/templates/template-task-locks.json", f"{phases['development']}/task_locks.json", "pm-po")
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
            content = content.replace("[ชื่องาน/ฟีเจอร์]", title)
            content = content.replace("[ชื่องาน]", title)
            
            # Write target file
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  [Created File] {target_rel}")
        except Exception as e:
            print(f"  [Error] Failed to create {target_rel}: {e}")

    print("\nDone! Please link the new feature on the project board:")
    print(f"second-brain/project_board.md -> | {current_date} | [[brd#{title}]] | Inbox | - |")

if __name__ == "__main__":
    main()
