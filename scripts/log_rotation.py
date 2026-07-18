import os
import shutil
from datetime import datetime

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INBOX_FILE = os.path.join(WORKSPACE_DIR, "second-brain", "01-inbox", "inbox_log.md")
INBOX_ARCHIVE = os.path.join(WORKSPACE_DIR, "second-brain", "10-archives", "inbox_archive.md")

TEST_LOG_FILE = os.path.join(WORKSPACE_DIR, "second-brain", "07-qa-testing", "test_execution.log")
TEST_LOG_ARCHIVE_DIR = os.path.join(WORKSPACE_DIR, "second-brain", "10-archives", "test_logs")
DIARY_DIR = os.path.join(WORKSPACE_DIR, "second-brain", "11-diary")
DIARY_ARCHIVE_DIR = os.path.join(WORKSPACE_DIR, "second-brain", "10-archives", "diary")

INBOX_MAX_LINES = 200
TEST_LOG_MAX_LINES = 1000

def rotate_inbox():
    if not os.path.exists(INBOX_FILE):
        return
    
    with open(INBOX_FILE, 'r') as f:
        lines = f.readlines()
        
    if len(lines) > INBOX_MAX_LINES:
        # Keep the header and top entries (first INBOX_MAX_LINES lines)
        # Move the rest to archive
        keep_lines = lines[:INBOX_MAX_LINES]
        archive_lines = lines[INBOX_MAX_LINES:]
        
        with open(INBOX_FILE, 'w') as f:
            f.writelines(keep_lines)
            
        with open(INBOX_ARCHIVE, 'a') as f:
            f.write(f"\n\n--- Archived on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
            f.writelines(archive_lines)
        print(f"Rotated {len(archive_lines)} lines from inbox_log.md to inbox_archive.md")

def rotate_test_log():
    if not os.path.exists(TEST_LOG_FILE):
        return
        
    with open(TEST_LOG_FILE, 'r') as f:
        lines = f.readlines()
        
    if len(lines) > TEST_LOG_MAX_LINES:
        os.makedirs(TEST_LOG_ARCHIVE_DIR, exist_ok=True)
        archive_name = os.path.join(TEST_LOG_ARCHIVE_DIR, f"test_execution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        shutil.move(TEST_LOG_FILE, archive_name)
        # Touch new file
        with open(TEST_LOG_FILE, 'w') as f:
            f.write("--- New Test Execution Log ---\n")
        print(f"Rotated test_execution.log to {archive_name}")

def rotate_diary():
    if not os.path.exists(DIARY_DIR):
        return
    
    os.makedirs(DIARY_ARCHIVE_DIR, exist_ok=True)
    today = datetime.now()
    
    for filename in os.listdir(DIARY_DIR):
        if not filename.endswith(".md") or filename == ".gitkeep":
            continue
            
        # Filename starts with YYYY-MM-DD (length 10)
        if len(filename) >= 10:
            date_str = filename[:10]
            try:
                file_date = datetime.strptime(date_str, "%Y-%m-%d")
                age_days = (today - file_date).days
                if age_days > 30:
                    src_path = os.path.join(DIARY_DIR, filename)
                    dest_path = os.path.join(DIARY_ARCHIVE_DIR, filename)
                    shutil.move(src_path, dest_path)
                    print(f"Archived old diary file: {filename} to archives/diary/")
            except ValueError:
                # Filename does not start with a valid YYYY-MM-DD date
                continue

if __name__ == "__main__":
    rotate_inbox()
    rotate_test_log()
    rotate_diary()
