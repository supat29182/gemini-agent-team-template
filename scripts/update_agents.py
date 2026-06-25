import os
import glob

agent_dir = "/Users/phukit.but.adm/Desktop/gemini-agent/gemini-agent-team-template/.agents/agents"
files = glob.glob(os.path.join(agent_dir, "*.md"))

instruction = "\n> [!TIP]\n> **Nexus Librarian (GitNexus)**: เมื่อต้องการสืบค้นโค้ด, โครงสร้างระบบ, หรือหาเอกสารอ้างอิงที่ซับซ้อน ให้เรียกใช้งาน tool `nexus-librarian` เพื่อดึงข้อมูลจากระบบเบื้องหลังก่อนตัดสินใจลงมือเสมอ\n"

for f in files:
    if "nexus-librarian.md" in f:
        continue
    with open(f, "r") as file:
        content = file.read()
    
    if "- nexus-librarian" not in content:
        # insert into tools:
        if "tools:\n" in content:
            content = content.replace("tools:\n", "tools:\n  - nexus-librarian\n")
        
        # append instruction at the end of the file
        content += instruction
        
        with open(f, "w") as file:
            file.write(content)
        print(f"Updated {f}")
    else:
        print(f"Skipped {f}")
