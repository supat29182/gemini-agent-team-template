#!/usr/bin/env python3
import os
import sys
import argparse
import datetime
import re

def get_current_date():
    return datetime.date.today().strftime("%Y-%m-%d")

def split_markdown_row(row):
    parts = []
    current = []
    in_brackets = 0
    for char in row:
        if char == '[':
            in_brackets += 1
            current.append(char)
        elif char == ']':
            in_brackets = max(0, in_brackets - 1)
            current.append(char)
        elif char == '|' and in_brackets == 0:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    parts.append("".join(current).strip())
    return parts

def main():
    parser = argparse.ArgumentParser(description="Deterministic manager for the Project Board markdown table")
    parser.add_argument("--action", required=True, choices=["add", "update"], help="Action to perform")
    parser.add_argument("--slug", required=True, help="Task folder slug (e.g. line-notify)")
    parser.add_argument("--title", help="Task title (required for 'add')")
    parser.add_argument("--type", choices=["feature", "cr", "bug"], default="feature", help="Task type (required for 'add')")
    parser.add_argument("--status", choices=["[Inbox]", "[Phase 1] Design", "[Phase 2] Implementation", "[Phase 3] QA", "[Done]"], help="New status (required for 'update')")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_dir = os.path.abspath(os.path.join(script_dir, ".."))
    board_path = os.path.join(workspace_dir, "second-brain/project_board.md")

    if not os.path.exists(board_path):
        print(f"Error: Project Board file not found at {board_path}", file=sys.stderr)
        sys.exit(1)

    with open(board_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.splitlines()
    table_start_idx = -1
    table_header_pattern = re.compile(r"^\|\s*Date\s*\|\s*Task Name")

    for idx, line in enumerate(lines):
        if table_header_pattern.search(line):
            table_start_idx = idx
            break

    if table_start_idx == -1:
        print("Error: Could not find the Kanban board table in project_board.md", file=sys.stderr)
        sys.exit(1)

    # The table separator is expected at table_start_idx + 1
    if table_start_idx + 1 >= len(lines) or not lines[table_start_idx + 1].strip().startswith("|"):
        print("Error: Invalid table format (missing separator line)", file=sys.stderr)
        sys.exit(1)

    table_data_start = table_start_idx + 2
    
    # We find all subsequent lines that are part of the table
    table_end_idx = table_data_start
    while table_end_idx < len(lines) and lines[table_end_idx].strip().startswith("|"):
        table_end_idx += 1

    table_rows = lines[table_data_start:table_end_idx]

    current_date = get_current_date()

    if args.action == "add":
        if not args.title:
            print("Error: --title is required for 'add' action", file=sys.stderr)
            sys.exit(1)

        # Check if the slug already exists in any of the rows
        slug_pattern = re.compile(rf"/{args.slug}/")
        for row in table_rows:
            if slug_pattern.search(row):
                print(f"Warning: Task with slug '{args.slug}' already exists on the project board. Skipping add.")
                sys.exit(0)

        # Form the path
        folder_type = "features"
        if args.type == "cr":
            folder_type = "cr"
        elif args.type == "bug":
            folder_type = "bug"

        if args.type == "bug":
            link_path = f"second-brain/20-architecture/bug/{args.slug}/bug_diagnosis.md"
        else:
            link_path = f"second-brain/10-requirements-spec/{folder_type}/{args.slug}/brd.md"

        link_text = f"[[{link_path}|{args.title}]]"
        new_row = f"| {current_date} | {link_text} | [Inbox] | {current_date} |"
        
        # Append new row
        lines.insert(table_end_idx, new_row)
        print(f"Added task '{args.title}' with slug '{args.slug}' to project board.")

    elif args.action == "update":
        if not args.status:
            print("Error: --status is required for 'update' action", file=sys.stderr)
            sys.exit(1)

        slug_pattern = re.compile(rf"/{args.slug}/")
        row_found_idx = -1
        
        for idx in range(table_data_start, table_end_idx):
            if slug_pattern.search(lines[idx]):
                row_found_idx = idx
                break

        if row_found_idx == -1:
            print(f"Error: Task with slug '{args.slug}' not found on the project board", file=sys.stderr)
            sys.exit(1)

        # Parse existing row columns
        columns = split_markdown_row(lines[row_found_idx])
        # row looks like: | Date | Task Link | Current Status | Last Updated |
        # split gives ['', 'Date', 'Task Link', 'Current Status', 'Last Updated', '']
        if len(columns) < 5:
            print(f"Error: Malformed row at line {row_found_idx + 1}: {lines[row_found_idx]}", file=sys.stderr)
            sys.exit(1)

        columns[3] = args.status
        columns[4] = current_date
        
        updated_row = "| " + " | ".join(columns[1:-1]) + " |"
        lines[row_found_idx] = updated_row
        print(f"Updated status of task '{args.slug}' to '{args.status}' on project board.")

    # Write back
    with open(board_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines) + "\n")

if __name__ == "__main__":
    main()
