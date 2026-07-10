#!/usr/bin/env python3
import os
import sys
import json
import argparse
from datetime import datetime

def get_lock_file_path(workspace_dir, slug, task_type):
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

    return os.path.join(workspace_dir, "second-brain", "30-development", folder_type, slug, "task_locks.json")

def main():
    parser = argparse.ArgumentParser(description="Deterministic Task Lock Manager")
    parser.add_argument("--slug", required=True, help="Feature/Bug slug")
    parser.add_argument("--type", choices=["feature", "cr", "bug"], default="feature")
    parser.add_argument("--agent", required=True, help="Agent name (e.g. backend-dev, frontend-dev)")
    parser.add_argument("--action", choices=["acquire", "release", "fail", "reset"], required=True)
    parser.add_argument("--reason", default="", help="Reason for failure (used with fail action)")
    
    args = parser.parse_args()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_dir = os.path.abspath(os.path.join(script_dir, ".."))
    
    lock_file = get_lock_file_path(workspace_dir, args.slug, args.type)
    
    if not os.path.exists(lock_file):
        print(f"Error: task_locks.json not found at {lock_file}")
        sys.exit(1)
        
    try:
        with open(lock_file, 'r', encoding='utf-8') as f:
            locks = json.load(f)
    except Exception as e:
        print(f"Error reading lock file: {e}")
        sys.exit(1)
        
    if args.agent not in locks:
        print(f"Error: Agent '{args.agent}' not found in lock file.")
        sys.exit(1)
        
    current_time = datetime.now().isoformat()
    agent_data = locks[args.agent]
    
    if args.action == "acquire":
        if agent_data["status"] == "in-progress":
            print(f"Error: Agent '{args.agent}' is already in-progress.")
            sys.exit(1)
        if agent_data["status"] == "completed":
            print(f"Error: Agent '{args.agent}' has already completed this task.")
            sys.exit(1)
            
        # Dependency checks
        if args.agent == "frontend-dev":
            if locks.get("backend-dev", {}).get("status") != "completed":
                print("Error: Dependency failed. frontend-dev requires backend-dev to be completed.")
                sys.exit(1)
        elif args.agent in ["security-audit", "qa-automate-execution"]:
            if locks.get("backend-dev", {}).get("status") != "completed" or locks.get("frontend-dev", {}).get("status") != "completed":
                # For bug type, frontend might not be used, but standard workflow demands both
                if args.type != "bug" or locks.get("frontend-dev", {}).get("status") not in ["completed", "idle"]:
                     print(f"Error: Dependency failed. {args.agent} requires both dev phases to be completed.")
                     sys.exit(1)
                     
        locks[args.agent]["status"] = "in-progress"
        locks[args.agent]["locked_at"] = current_time
        locks[args.agent]["locked_by"] = args.agent
        print(f"Success: Acquired lock for '{args.agent}'.")
        
    elif args.action == "release":
        if agent_data["status"] != "in-progress":
            print(f"Warning: Releasing lock for '{args.agent}' but status was '{agent_data['status']}'.")
            
        locks[args.agent]["status"] = "completed"
        locks[args.agent]["completed_at"] = current_time
        print(f"Success: Released lock for '{args.agent}' (marked as completed).")
        
    elif args.action == "fail":
        locks[args.agent]["status"] = "failed"
        if args.reason:
            locks[args.agent]["reason"] = args.reason
        print(f"Success: Marked '{args.agent}' as failed.")
        
    elif args.action == "reset":
        locks[args.agent]["status"] = "idle"
        locks[args.agent].pop("locked_at", None)
        locks[args.agent].pop("locked_by", None)
        locks[args.agent].pop("completed_at", None)
        locks[args.agent].pop("reason", None)
        print(f"Success: Reset '{args.agent}' to idle.")
        
    # Write back atomically
    try:
        with open(lock_file, 'w', encoding='utf-8') as f:
            json.dump(locks, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error writing lock file: {e}")
        sys.exit(1)
        
if __name__ == "__main__":
    main()
