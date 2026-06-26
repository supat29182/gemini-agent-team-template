import os
import shutil
from datetime import datetime

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INBOX_FILE = os.path.join(WORKSPACE_DIR, "second-brain", "00-inbox", "inbox_log.md")
INBOX_ARCHIVE = os.path.join(WORKSPACE_DIR, "second-brain", "archives", "inbox_archive.md")

TEST_LOG_FILE = os.path.join(WORKSPACE_DIR, "second-brain", "50-qa-testing", "test_execution.log")
TEST_LOG_ARCHIVE_DIR = os.path.join(WORKSPACE_DIR, "second-brain", "archives", "test_logs")

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

if __name__ == "__main__":
    rotate_inbox()
    rotate_test_log()
