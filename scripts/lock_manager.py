#!/usr/bin/env python3
import os
import sys
import json
import argparse
import re
import yaml
from datetime import datetime

def validate_uxui_stitch_references(workspace_dir, slug, task_type):
    folder_type = "features"
    if task_type == "cr":
        folder_type = "cr"
        if not slug.startswith("cr-"): slug = f"cr-{slug}"
    elif task_type == "bug":
        folder_type = "bug"
        if not slug.startswith("bug-"): slug = f"bug-{slug}"
    else:
        slug = slug.replace("cr-", "").replace("bug-", "")

    spec_path = os.path.join(workspace_dir, "second-brain", "03-requirements-spec", folder_type, slug, "design_spec.md")
    if not os.path.exists(spec_path):
        return False, f"Missing design_spec.md at {spec_path}"

    try:
        with open(spec_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"Could not read design_spec.md: {e}"

    if "Stitch Project References" not in content and "Stitch Project ID" not in content:
        return False, "design_spec.md does not contain a 'Stitch Project References' section."

    project_id_match = re.search(r'Stitch Project ID\b[^|]*\|\s*`?([^`\s|<>]+)`?', content, re.IGNORECASE)
    if not project_id_match:
        return False, "Could not find a valid 'Stitch Project ID' in design_spec.md."

    pid = project_id_match.group(1).strip()
    if not pid or pid.lower() in ["<project_id>", "n/a", "none", "null", "placeholder"]:
        return False, f"Invalid or placeholder Stitch Project ID found: '{pid}'"

    return True, "Valid Stitch references found."

def validate_qa_playwright_references(workspace_dir, slug, task_type):
    folder_type = "features"
    if task_type == "cr":
        folder_type = "cr"
        if not slug.startswith("cr-"): slug = f"cr-{slug}"
    elif task_type == "bug":
        folder_type = "bug"
        if not slug.startswith("bug-"): slug = f"bug-{slug}"
    else:
        slug = slug.replace("cr-", "").replace("bug-", "")

    design_spec_path = os.path.join(workspace_dir, "second-brain", "03-requirements-spec", folder_type, slug, "design_spec.md")
    if not os.path.exists(design_spec_path):
        return True, "Non-UI task (no design_spec.md), Playwright check bypassed."

    exec_path = os.path.join(workspace_dir, "second-brain", "07-qa-testing", folder_type, slug, "test_execution.md")
    if not os.path.exists(exec_path):
        return False, f"Missing test_execution.md for UI task at {exec_path}"

    try:
        with open(exec_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"Could not read test_execution.md: {e}"

    playwright_keywords = [
        "playwright", "mcp_playwright", "browser", "page.navigate", "page.click",
        "navigate", "screenshot", "chromium", "firefox", "webkit", "headless"
    ]

    has_evidence = any(kw in content.lower() for kw in playwright_keywords)
    if not has_evidence:
        return False, "test_execution.md for UI task does not contain evidence of Playwright MCP browser test execution."

    return True, "Valid Playwright execution evidence found."

def validate_security_audit_references(workspace_dir, slug, task_type):
    folder_type = "features"
    if task_type == "cr":
        folder_type = "cr"
        if not slug.startswith("cr-"): slug = f"cr-{slug}"
    elif task_type == "bug":
        folder_type = "bug"
        if not slug.startswith("bug-"): slug = f"bug-{slug}"
    else:
        slug = slug.replace("cr-", "").replace("bug-", "")

    audit_path = os.path.join(workspace_dir, "second-brain", "06-security", folder_type, slug, "security_audit.md")
    if not os.path.exists(audit_path):
        return False, f"Missing security_audit.md at {audit_path}"

    try:
        with open(audit_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"Could not read security_audit.md: {e}"

    if "[STATUS: PASSED]" not in content and "[STATUS: FAILED]" not in content:
        return False, "security_audit.md is missing explicit '[STATUS: PASSED]' or '[STATUS: FAILED]' status header."

    return True, "Valid security audit status found."

def validate_architect_impact_references(workspace_dir, slug, task_type):
    folder_type = "features"
    if task_type == "cr":
        folder_type = "cr"
        if not slug.startswith("cr-"): slug = f"cr-{slug}"
    elif task_type == "bug":
        folder_type = "bug"
        if not slug.startswith("bug-"): slug = f"bug-{slug}"
    else:
        slug = slug.replace("cr-", "").replace("bug-", "")

    impact_path = os.path.join(workspace_dir, "second-brain", "04-architecture", folder_type, slug, "architecture_impact.md")
    if not os.path.exists(impact_path):
        return False, f"Missing architecture_impact.md at {impact_path}"

    try:
        with open(impact_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"Could not read architecture_impact.md: {e}"

    impact_keywords = ["blast radius", "impact", "gitnexus", "affected", "symbol"]
    has_impact_evidence = any(kw in content.lower() for kw in impact_keywords)
    if not has_impact_evidence:
        return False, "architecture_impact.md does not contain Blast Radius or GitNexus impact analysis details."

    return True, "Valid architecture impact analysis found."

def validate_sa_contract_references(workspace_dir, slug, task_type):
    folder_type = "features"
    if task_type == "cr":
        folder_type = "cr"
        if not slug.startswith("cr-"): slug = f"cr-{slug}"
    elif task_type == "bug":
        folder_type = "bug"
        if not slug.startswith("bug-"): slug = f"bug-{slug}"
    else:
        slug = slug.replace("cr-", "").replace("bug-", "")

    spec_path = os.path.join(workspace_dir, "second-brain", "03-requirements-spec", folder_type, slug, "system_spec.md")
    contract_path = os.path.join(workspace_dir, "second-brain", "03-requirements-spec", folder_type, slug, "api_contract.yaml")

    if not os.path.exists(spec_path):
        return False, f"Missing system_spec.md at {spec_path}"

    if not os.path.exists(contract_path):
        return False, f"Missing api_contract.yaml at {contract_path}"

    try:
        with open(contract_path, 'r', encoding='utf-8') as f:
            yaml.safe_load(f)
    except Exception as e:
        return False, f"api_contract.yaml contains invalid YAML syntax: {e}"

    return True, "Valid SA specs and API contract found."

def validate_dev_changelog_references(workspace_dir, slug, agent):
    changelog_dir = os.path.join(workspace_dir, "second-brain", "10-archives", "changelog")
    if not os.path.exists(changelog_dir):
        return False, f"Changelog directory does not exist at {changelog_dir}"

    slug_clean = slug.replace("cr-", "").replace("bug-", "")
    found = False
    try:
        for filename in os.listdir(changelog_dir):
            if filename.endswith(".md") and (slug in filename or slug_clean in filename):
                found = True
                break
    except Exception as e:
        return False, f"Could not scan changelog directory: {e}"

    if not found:
        return False, f"Missing changelog entry for '{slug}' in second-brain/10-archives/changelog/"

    return True, f"Valid changelog entry found for {agent}."

def get_paths(workspace_dir, slug, task_type):
    folder_type = "features"
    if task_type == "cr":
        folder_type = "cr"
        if not slug.startswith("cr-"): slug = f"cr-{slug}"
    elif task_type == "bug":
        folder_type = "bug"
        if not slug.startswith("bug-"): slug = f"bug-{slug}"
    else:
        # Default feature, remove cr/bug prefix if mistakenly provided
        slug = slug.replace("cr-", "").replace("bug-", "")

    dev_dir = os.path.join(workspace_dir, "second-brain", "05-development", folder_type, slug)
    locks_dir = os.path.join(dev_dir, "locks")
    legacy_file = os.path.join(dev_dir, "task_locks.json")

    return dev_dir, locks_dir, legacy_file

def read_lock_status(locks_dir, legacy_file, agent, is_decentralized):
    if is_decentralized:
        agent_file = os.path.join(locks_dir, f"{agent}.json")
        if not os.path.exists(agent_file):
            return None
        try:
            with open(agent_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading lock file for '{agent}': {e}")
            sys.exit(1)
    else:
        if not os.path.exists(legacy_file):
            return None
        try:
            with open(legacy_file, 'r', encoding='utf-8') as f:
                locks = json.load(f)
                return locks.get(agent)
        except Exception as e:
            print(f"Error reading legacy lock file: {e}")
            sys.exit(1)

def write_lock_status(locks_dir, legacy_file, agent, data, is_decentralized):
    if is_decentralized:
        os.makedirs(locks_dir, exist_ok=True)
        agent_file = os.path.join(locks_dir, f"{agent}.json")
        tmp_file = f"{agent_file}.tmp"
        try:
            with open(tmp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            os.replace(tmp_file, agent_file) # Atomic rename (replace target file atomically)
        except Exception as e:
            if os.path.exists(tmp_file):
                try: os.remove(tmp_file)
                except: pass
            print(f"Error writing lock file for '{agent}': {e}")
            sys.exit(1)
    else:
        tmp_file = f"{legacy_file}.tmp"
        try:
            locks = {}
            if os.path.exists(legacy_file):
                with open(legacy_file, 'r', encoding='utf-8') as f:
                    locks = json.load(f)
            locks[agent] = data
            with open(tmp_file, 'w', encoding='utf-8') as f:
                json.dump(locks, f, indent=2, ensure_ascii=False)
            os.replace(tmp_file, legacy_file) # Atomic rename
        except Exception as e:
            if os.path.exists(tmp_file):
                try: os.remove(tmp_file)
                except: pass
            print(f"Error writing legacy lock file: {e}")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Deterministic and Race-Condition Safe Task Lock Manager")
    parser.add_argument("--slug", required=True, help="Feature/Bug slug")
    parser.add_argument("--type", choices=["feature", "cr", "bug"], default="feature")
    parser.add_argument("--agent", required=False, help="Agent name (e.g. backend-dev, frontend-dev, qa-test-plan, security-audit, qa-automate-execution)")
    parser.add_argument("--action", choices=["acquire", "release", "fail", "reset", "status-all", "skip"], required=True)
    parser.add_argument("--reason", default="", help="Reason for failure (used with fail action)")
    
    args = parser.parse_args()
    
    if args.action != "status-all" and not args.agent:
        parser.error("--agent is required for actions other than status-all")
        
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_dir = os.path.abspath(os.path.join(script_dir, ".."))
    
    dev_dir, locks_dir, legacy_file = get_paths(workspace_dir, args.slug, args.type)
    
    is_decentralized = os.path.exists(locks_dir)
    
    # Validation: Ensure at least one lock configuration exists
    if not is_decentralized and not os.path.exists(legacy_file):
        print(f"Error: Neither decentralized 'locks' folder nor 'task_locks.json' found in {dev_dir}")
        sys.exit(1)
        
    current_time = datetime.now().isoformat()
    
    default_ttls = {
        "sa": 30,
        "ux-ui": 40,
        "solution-architect": 30,
        "backend-dev": 45,
        "frontend-dev": 45,
        "qa-test-plan": 35,
        "security-audit": 25,
        "qa-automate-execution": 35
    }

    if args.action == "status-all":
        agents_list = ["sa", "ux-ui", "solution-architect", "backend-dev", "frontend-dev", "qa-test-plan", "security-audit", "qa-automate-execution"]
        summary = {}
        for ag in agents_list:
            ag_data = read_lock_status(locks_dir, legacy_file, ag, is_decentralized)
            if not ag_data:
                ag_data = {
                    "status": "idle",
                    "locked_by": "",
                    "locked_at": "",
                    "completed_at": "",
                    "ttl_mins": default_ttls.get(ag, 30)
                }
            if ag_data.get("status") == "in-progress" and ag_data.get("locked_at"):
                try:
                    locked_at_dt = datetime.fromisoformat(ag_data["locked_at"])
                    elapsed_mins = (datetime.now() - locked_at_dt).total_seconds() / 60.0
                    if elapsed_mins > ag_data.get("ttl_mins", 30):
                        ag_data["ttl_exceeded"] = True
                        ag_data["elapsed_mins"] = round(elapsed_mins, 1)
                except Exception:
                    pass
            summary[ag] = ag_data
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        sys.exit(0)
        
    agent_data = read_lock_status(locks_dir, legacy_file, args.agent, is_decentralized)
    
    if not agent_data:
        # Lazy initialization
        agent_data = {
            "status": "idle",
            "locked_by": "",
            "locked_at": "",
            "completed_at": "",
            "ttl_mins": default_ttls.get(args.agent, 30)
        }
        
    if args.action == "acquire":
        if agent_data.get("status") == "in-progress":
            print(f"Error: Agent '{args.agent}' is already in-progress.")
            sys.exit(1)
        if agent_data.get("status") == "completed":
            print(f"Error: Agent '{args.agent}' has already completed this task.")
            sys.exit(1)
            
        # Dependency checks
        if args.agent == "ux-ui":
            sa_status = read_lock_status(locks_dir, legacy_file, "sa", is_decentralized)
            if sa_status and sa_status.get("status") != "completed":
                print("Error: Dependency failed. ux-ui requires sa to be completed.")
                sys.exit(1)
        elif args.agent == "solution-architect":
            sa_status = read_lock_status(locks_dir, legacy_file, "sa", is_decentralized)
            if sa_status and sa_status.get("status") != "completed":
                print("Error: Dependency failed. solution-architect requires sa to be completed.")
                sys.exit(1)
            uxui_status = read_lock_status(locks_dir, legacy_file, "ux-ui", is_decentralized)
            if uxui_status and uxui_status.get("status") not in ["completed", "skipped"]:
                print("Error: Dependency failed. solution-architect requires ux-ui to be completed or skipped.")
                sys.exit(1)
        elif args.agent == "backend-dev":
            sa_arch_status = read_lock_status(locks_dir, legacy_file, "solution-architect", is_decentralized)
            if sa_arch_status and sa_arch_status.get("status") not in ["completed", "skipped"]:
                print("Error: Dependency failed. backend-dev requires solution-architect to be completed or skipped.")
                sys.exit(1)
        elif args.agent == "frontend-dev":
            uxui_status = read_lock_status(locks_dir, legacy_file, "ux-ui", is_decentralized)
            if not uxui_status or uxui_status.get("status") not in ["completed", "skipped"]:
                print("Error: Dependency failed. frontend-dev requires ux-ui to be completed or skipped.")
                sys.exit(1)
            backend_status = read_lock_status(locks_dir, legacy_file, "backend-dev", is_decentralized)
            if not backend_status or backend_status.get("status") != "completed":
                print("Error: Dependency failed. frontend-dev requires backend-dev to be completed.")
                sys.exit(1)
        elif args.agent in ["security-audit", "qa-automate-execution"]:
            backend_status = read_lock_status(locks_dir, legacy_file, "backend-dev", is_decentralized)
            frontend_status = read_lock_status(locks_dir, legacy_file, "frontend-dev", is_decentralized)
            
            backend_ok = backend_status and backend_status.get("status") == "completed"
            
            # For non-bug tasks, frontend-dev must be completed or skipped (not idle)
            frontend_ok = False
            if frontend_status:
                allowed_frontend = ["completed", "skipped", "idle"] if args.type == "bug" else ["completed", "skipped"]
                frontend_ok = frontend_status.get("status") in allowed_frontend
            else:
                if args.type == "bug":
                    frontend_ok = True
                     
            if not backend_ok or not frontend_ok:
                print(f"Error: Dependency failed. {args.agent} requires both dev phases to be completed.")
                sys.exit(1)
                
        agent_data["status"] = "in-progress"
        agent_data["locked_at"] = current_time
        agent_data["locked_by"] = args.agent
        print(f"Success: Acquired lock for '{args.agent}'.")
        
    elif args.action == "release":
        if args.agent == "ux-ui":
            valid, msg = validate_uxui_stitch_references(workspace_dir, args.slug, args.type)
            if not valid:
                print(f"Error: Mandatory Stitch Gate failed for ux-ui release: {msg}")
                sys.exit(1)
        elif args.agent == "qa-automate-execution":
            valid, msg = validate_qa_playwright_references(workspace_dir, args.slug, args.type)
            if not valid:
                print(f"Error: Mandatory Playwright Gate failed for qa-automate-execution release: {msg}")
                sys.exit(1)
        elif args.agent == "security-audit":
            valid, msg = validate_security_audit_references(workspace_dir, args.slug, args.type)
            if not valid:
                print(f"Error: Mandatory Security Gate failed for security-audit release: {msg}")
                sys.exit(1)
        elif args.agent == "solution-architect":
            valid, msg = validate_architect_impact_references(workspace_dir, args.slug, args.type)
            if not valid:
                print(f"Error: Mandatory Architect Impact Gate failed for solution-architect release: {msg}")
                sys.exit(1)
        elif args.agent == "sa":
            valid, msg = validate_sa_contract_references(workspace_dir, args.slug, args.type)
            if not valid:
                print(f"Error: Mandatory SA Spec & Contract Gate failed for sa release: {msg}")
                sys.exit(1)
        elif args.agent in ["backend-dev", "frontend-dev"]:
            valid, msg = validate_dev_changelog_references(workspace_dir, args.slug, args.agent)
            if not valid:
                print(f"Error: Mandatory Changelog Gate failed for {args.agent} release: {msg}")
                sys.exit(1)

        if agent_data.get("status") != "in-progress":
            print(f"Warning: Releasing lock for '{args.agent}' but status was '{agent_data.get('status')}'.")
            
        agent_data["status"] = "completed"
        agent_data["completed_at"] = current_time
        print(f"Success: Released lock for '{args.agent}' (marked as completed).")
        
    elif args.action == "fail":
        agent_data["status"] = "failed"
        if args.reason:
            agent_data["reason"] = args.reason
        print(f"Success: Marked '{args.agent}' as failed.")

    elif args.action == "skip":
        agent_data["status"] = "skipped"
        if args.reason:
            agent_data["reason"] = args.reason
        else:
            agent_data["reason"] = "Skipped by PM"
        print(f"Success: Marked '{args.agent}' as skipped.")
        
    elif args.action == "reset":
        agent_data["status"] = "idle"
        agent_data.pop("locked_at", None)
        agent_data.pop("locked_by", None)
        agent_data.pop("completed_at", None)
        agent_data.pop("reason", None)
        print(f"Success: Reset '{args.agent}' to idle.")
        
    # Write updated lock data back atomically
    write_lock_status(locks_dir, legacy_file, args.agent, agent_data, is_decentralized)

if __name__ == "__main__":
    main()
