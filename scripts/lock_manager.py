#!/usr/bin/env python3
import os
import sys
import json
import argparse
from datetime import datetime

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

    dev_dir = os.path.join(workspace_dir, "second-brain", "30-development", folder_type, slug)
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
    parser.add_argument("--agent", required=True, help="Agent name (e.g. backend-dev, frontend-dev, qa-test-plan, security-audit, qa-automate-execution)")
    parser.add_argument("--action", choices=["acquire", "release", "fail", "reset"], required=True)
    parser.add_argument("--reason", default="", help="Reason for failure (used with fail action)")
    
    args = parser.parse_args()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_dir = os.path.abspath(os.path.join(script_dir, ".."))
    
    dev_dir, locks_dir, legacy_file = get_paths(workspace_dir, args.slug, args.type)
    
    is_decentralized = os.path.exists(locks_dir)
    
    # Validation: Ensure at least one lock configuration exists
    if not is_decentralized and not os.path.exists(legacy_file):
        print(f"Error: Neither decentralized 'locks' folder nor 'task_locks.json' found in {dev_dir}")
        sys.exit(1)
        
    current_time = datetime.now().isoformat()
    
    agent_data = read_lock_status(locks_dir, legacy_file, args.agent, is_decentralized)
    
    if not agent_data:
        # Lazy initialization
        default_ttls = {
            "backend-dev": 45,
            "frontend-dev": 45,
            "qa-test-plan": 35,
            "security-audit": 25,
            "qa-automate-execution": 35
        }
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
        if args.agent == "frontend-dev":
            backend_status = read_lock_status(locks_dir, legacy_file, "backend-dev", is_decentralized)
            if not backend_status or backend_status.get("status") != "completed":
                print("Error: Dependency failed. frontend-dev requires backend-dev to be completed.")
                sys.exit(1)
        elif args.agent in ["security-audit", "qa-automate-execution"]:
            backend_status = read_lock_status(locks_dir, legacy_file, "backend-dev", is_decentralized)
            frontend_status = read_lock_status(locks_dir, legacy_file, "frontend-dev", is_decentralized)
            
            backend_ok = backend_status and backend_status.get("status") == "completed"
            
            # For bug type, frontend-dev might be skipped or completed
            frontend_ok = False
            if frontend_status:
                frontend_ok = frontend_status.get("status") in ["completed", "skipped", "idle"]
            else:
                # If frontend-dev file does not exist, check if it's bug type
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
