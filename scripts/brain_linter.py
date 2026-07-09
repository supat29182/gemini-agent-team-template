#!/usr/bin/env python3
"""
Brain Linter — ตรวจสอบความสมบูรณ์ของ Second Brain
- Wikilinks (broken file links, broken heading references)
- YAML Frontmatter (missing frontmatter, missing tags, invalid tags)
- Orphan files (files not linked from anywhere)
"""
import os
import re
import sys
import yaml

# Regex to find [[wikilinks]]
WIKILINK_RE = re.compile(r'\[\[([^\]]+)\]\]')

# Frontmatter regex
FRONTMATTER_RE = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)

# Valid tags from tagging-policy.md
VALID_TAG_PREFIXES = {'doc/', 'phase/'}
VALID_TAGS = {
    'doc/index', 'doc/adr', 'doc/changelog',
    'doc/kb', 'doc/diary', 'doc/snapshot',
    'doc/spec', 'doc/eval', 'doc/postmortem',
    'doc/brd', 'doc/user-story', 'doc/dev-plan',
    'doc/architecture',
    'phase/inbox', 'phase/design', 'phase/implement',
    'phase/verify', 'phase/ship', 'phase/initiation',
}

# Files/dirs to skip frontmatter check
SKIP_FRONTMATTER = {
    '00-Index.md', 'README.md', 'project_board.md',
    'inbox_log.md', 'tagging-policy.md', 'AGENTS.md',
}

def clean_heading(heading_text):
    text = heading_text.lstrip('#').strip().lower()
    text = re.sub(r'[*_`]', '', text)
    return text

def build_index(root_dir, workspace_dir=None):
    file_map = {}
    headings_map = {}
    
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.md'):
                full_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(full_path, root_dir)
                basename = os.path.splitext(filename)[0].lower()
                file_map.setdefault(basename, []).append(rel_path)
                
                headings = set()
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            if line.strip().startswith('#'):
                                header = line.strip()
                                headings.add(clean_heading(header))
                except Exception as e:
                    print(f"Warning: Could not read headings from {rel_path}: {e}")
                
                headings_map[rel_path] = headings
                
    if workspace_dir:
        agents_md = os.path.join(workspace_dir, '.agents', 'AGENTS.md')
        if os.path.exists(agents_md):
            rel_path = '../.agents/AGENTS.md'
            basename = 'agents'
            file_map.setdefault(basename, []).append(rel_path)
            
            headings = set()
            try:
                with open(agents_md, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip().startswith('#'):
                            header = line.strip()
                            headings.add(clean_heading(header))
            except Exception as e:
                print(f"Warning: Could not read headings from AGENTS.md: {e}")
            headings_map[rel_path] = headings
            
    return file_map, headings_map

def scan_for_secrets(content, rel_file_path):
    """สแกนหา API Keys หรือความลับ (Secrets) ที่อาจรั่วไหลในไฟล์"""
    errors = []
    
    # Pattern 1: OpenAI API Key
    openai_key_re = re.compile(r'\bsk-[a-zA-Z0-9]{32,}\b|\bsk-proj-[a-zA-Z0-9_-]{40,}\b')
    # Pattern 2: Gemini / Google API Key
    google_key_re = re.compile(r'\bAIzaSy[a-zA-Z0-9_-]{33}\b')
    # Pattern 3: Generic password/token assignment with actual non-placeholder value
    generic_secret_re = re.compile(
        r'\b(?:password|passwd|secret|api_key|token|private_key|client_secret)\s*[:=]\s*["\']([^"\'\s]{8,})["\']',
        re.IGNORECASE
    )
    
    placeholders = {
        'placeholder', 'your_password', 'your_api_key', 'your-api-key', 'secretvalue', 
        'xxxx', 'yyyy', 'zzzz', '12345678', 'mypassword', 'password123', 'admin123',
        'enter_here', 'your_token', 'your-token', 'my-api-key'
    }
    
    for match in openai_key_re.findall(content):
        errors.append({
            'file': rel_file_path,
            'type': 'secret_leak_detected',
            'reason': f'พบ OpenAI API Key หรือร่องรอยคีย์ที่คล้ายกัน ({match[:6]}...) กรุณาลบออกเพื่อความปลอดภัย'
        })
        
    for match in google_key_re.findall(content):
        errors.append({
            'file': rel_file_path,
            'type': 'secret_leak_detected',
            'reason': f'พบ Google API Key หรือคีย์ Gemini ({match[:6]}...) กรุณาลบออกเพื่อความปลอดภัย'
        })
        
    for match in generic_secret_re.findall(content):
        val_lower = match.lower()
        if not any(pl in val_lower for pl in placeholders) and len(val_lower) > 7:
            errors.append({
                'file': rel_file_path,
                'type': 'secret_leak_detected',
                'reason': f'พบข้อมูลที่น่าจะเป็นความลับ (เช่น รหัสผ่าน หรือ API Key) ถูก Hardcoded: "...{match[-6:]}"'
            })
            
    return errors

def check_orphans(file_map, linked_basenames):
    """ตรวจสอบไฟล์ที่ไม่มีการเชื่อมโยงจากไฟล์อื่น (Orphan Files)"""
    errors = []
    
    # ไฟล์/ไดเรกทอรีที่ไม่จำเป็นต้องถูก Link ถึง
    exempt_basenames = {
        '00-index', 'readme', 'project_board', 
        'inbox_log', 'tagging-policy', 'agents',
    }
    
    for basename, paths in file_map.items():
        if basename in exempt_basenames:
            continue
        for rel_path in paths:
            if 'diary/' in rel_path or 'archives/' in rel_path or 'templates/' in rel_path or 'features/' in rel_path:
                continue
            
            if basename not in linked_basenames:
                errors.append({
                    'file': os.path.join('second-brain', rel_path),
                    'type': 'orphan_file',
                    'reason': 'ไฟล์นี้ไม่มีไฟล์อื่นใน Second Brain ชี้ลิงก์มาหาเลย (Orphan File) กรุณาเขียนลิงก์ระบุในดัชนีหรือไฟล์อ้างอิงหลัก'
                })
            
    return errors

def check_critical_files(workspace_dir):
    """ตรวจสอบการมีอยู่ของไฟล์และเทมเพลตสำคัญที่บอทจำเป็นต้องใช้"""
    errors = []
    critical_files = [
        'second-brain/00-Index.md',
        'second-brain/project_board.md',
        'second-brain/00-inbox/inbox_log.md',
        'second-brain/70-resources/templates/template-system-spec.md',
        'second-brain/70-resources/templates/template-changelog.md',
    ]
    
    for rel_path in critical_files:
        abs_path = os.path.join(workspace_dir, rel_path)
        if not os.path.exists(abs_path):
            errors.append({
                'file': rel_path,
                'type': 'missing_critical_file',
                'reason': f'ไฟล์หรือเทมเพลตสำคัญไม่มีอยู่จริง บอทอาจไม่สามารถเริ่มทำงานหรือทำตามแผนได้'
            })
            
    return errors

def check_links(root_dir, file_map, headings_map):
    errors = []
    total_links = 0
    linked_basenames = set()
    
    for basename, paths in file_map.items():
        for rel_path in paths:
            abs_path = os.path.join(root_dir, rel_path)
        try:
            with open(abs_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Scan for secrets
            secret_errors = scan_for_secrets(content, os.path.join('second-brain', rel_path))
            errors.extend(secret_errors)
                
            # ละเว้นข้อความใน Code Block และ Inline Code
            content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
            content = re.sub(r'`[^`\n]+`', '', content)
                
            matches = WIKILINK_RE.findall(content)
            for match in matches:
                total_links += 1
                
                # Split display text if any (e.g. [[LinkTarget|DisplayName]])
                clean_match = match
                if '|' in match:
                    clean_match, _ = match.split('|', 1)
                
                if '#' in clean_match:
                    file_part, heading_part = clean_match.split('#', 1)
                    file_part = file_part.strip()
                    heading_part = heading_part.strip()
                else:
                    file_part = clean_match.strip()
                    heading_part = None
                
                file_part_lower = file_part.lower()
                
                # Case 1: Local link [[#Heading]]
                if not file_part:
                    if heading_part:
                        clean_target_heading = clean_heading(heading_part)
                        if clean_target_heading not in headings_map[rel_path]:
                            errors.append({
                                'file': rel_path,
                                'link': match,
                                'type': 'broken_link',
                                'reason': f"Local heading '{heading_part}' not found in this file"
                            })
                    continue
                
                # Case 2: File link [[filename]] or [[filename#heading]]
                if file_part_lower not in file_map:
                    errors.append({
                        'file': rel_path,
                        'link': match,
                        'type': 'broken_link',
                        'reason': f"Target file '{file_part}' not found in Second Brain"
                    })
                else:
                    target_rel_paths = file_map[file_part_lower]
                    linked_basenames.add(file_part_lower)
                    if heading_part:
                        clean_target_heading = clean_heading(heading_part)
                        found_heading = False
                        for target_rel_path in target_rel_paths:
                            if clean_target_heading in headings_map[target_rel_path]:
                                found_heading = True
                                break
                        if not found_heading:
                            errors.append({
                                'file': rel_path,
                                'link': match,
                                'type': 'broken_link',
                                'reason': f"Heading '{heading_part}' not found in target file '{file_part_lower}'"
                            })
        except Exception as e:
            print(f"Error checking links in {rel_path}: {e}")
            
    return total_links, errors, linked_basenames

def check_frontmatter(root_dir, file_map):
    """ตรวจสอบ YAML Frontmatter ของทุกไฟล์ .md"""
    errors = []
    total_checked = 0
    
    for basename, paths in file_map.items():
        for rel_path in paths:
            filename = os.path.basename(rel_path)
            
            # ข้ามไฟล์ที่ไม่ต้องการ frontmatter
            if filename in SKIP_FRONTMATTER:
                continue
            
            # ข้ามไฟล์ใน templates/
            if 'templates/' in rel_path:
                continue
                
            abs_path = os.path.join(root_dir, rel_path)
            total_checked += 1
            
            try:
                with open(abs_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check frontmatter exists
                fm_match = FRONTMATTER_RE.match(content)
                if not fm_match:
                    errors.append({
                        'file': rel_path,
                        'type': 'missing_frontmatter',
                        'reason': 'File is missing YAML frontmatter (---)'
                    })
                    continue
                
                # Parse YAML
                try:
                    fm_data = yaml.safe_load(fm_match.group(1))
                except yaml.YAMLError as e:
                    errors.append({
                        'file': rel_path,
                        'type': 'invalid_frontmatter',
                        'reason': f'Invalid YAML frontmatter: {e}'
                    })
                    continue
                
                if not isinstance(fm_data, dict):
                    errors.append({
                        'file': rel_path,
                        'type': 'invalid_frontmatter',
                        'reason': 'Frontmatter is not a valid YAML mapping'
                    })
                    continue
                
                # Check tags exist
                tags = fm_data.get('tags', [])
                if not tags:
                    errors.append({
                        'file': rel_path,
                        'type': 'missing_tags',
                        'reason': 'Frontmatter has no "tags" field or tags list is empty'
                    })
                    continue
                
                if not isinstance(tags, list):
                    errors.append({
                        'file': rel_path,
                        'type': 'invalid_tags',
                        'reason': f'Tags should be a list, got {type(tags).__name__}'
                    })
                    continue
                
                # Check at least one doc/* tag
                has_doc_tag = any(t.startswith('doc/') for t in tags if isinstance(t, str))
                if not has_doc_tag:
                    errors.append({
                        'file': rel_path,
                        'type': 'missing_doc_tag',
                        'reason': 'Must have at least one "doc/*" tag (e.g. doc/spec, doc/kb)'
                    })
                
                # Check all tags are valid
                for tag in tags:
                    if not isinstance(tag, str):
                        errors.append({
                            'file': rel_path,
                            'type': 'invalid_tag',
                            'reason': f'Tag must be a string, got: {tag}'
                        })
                        continue
                    if tag != tag.lower():
                        errors.append({
                            'file': rel_path,
                            'type': 'invalid_tag',
                            'reason': f'Tag "{tag}" must be lowercase'
                        })
                    if tag not in VALID_TAGS:
                        has_valid_prefix = any(tag.startswith(p) for p in VALID_TAG_PREFIXES)
                        if has_valid_prefix:
                            errors.append({
                                'file': rel_path,
                                'type': 'unknown_tag',
                                'reason': f'Tag "{tag}" has valid prefix but is not in the allowed tag list. Allowed: {sorted(VALID_TAGS)}'
                            })
                        # Tags without doc/ or phase/ prefix are allowed (custom tags)
                        
            except Exception as e:
                print(f"Error checking frontmatter in {rel_path}: {e}")
    
    return total_checked, errors

def check_second_brain_absolute_paths(root_dir, file_map):
    """ตรวจสอบไฟล์ใน Second Brain เพื่อป้องกันการใช้ Absolute Path"""
    errors = []
    abs_path_re = re.compile(r'(?:file:///Users/|/Users/|file:///home/|/home/)(?!username\b)')
    
    for basename, paths in file_map.items():
        for rel_path in paths:
            abs_path = os.path.join(root_dir, rel_path)
        try:
            with open(abs_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if abs_path_re.search(content):
                errors.append({
                    'file': os.path.join('second-brain', rel_path),
                    'type': 'absolute_path_detected',
                    'reason': 'พบพาธระบบแบบ Absolute (เช่น /Users/ หรือ /home/) กรุณาเปลี่ยนเป็น Relative Path เพื่อรองรับการทำงานร่วมกัน'
                })
        except Exception as e:
            print(f"Error checking absolute paths in {rel_path}: {e}")
            
    return errors

def check_agent_configurations(workspace_dir):
    """ตรวจสอบไฟล์ตั้งค่าบอทใน .agents/agents/ เพื่อหา absolute path และเช็คลิงก์เสีย"""
    errors = []
    agents_dir = os.path.join(workspace_dir, '.agents', 'agents')
    if not os.path.exists(agents_dir):
        return 0, errors
        
    total_checked = 0
    abs_path_re = re.compile(r'(?:file:///Users/|/Users/|file:///home/|/home/)(?!username\b)')
    skill_link_re = re.compile(r'\[[^\]]+\]\(([^)]+)\)')

    for filename in os.listdir(agents_dir):
        if filename.endswith('.md'):
            file_path = os.path.join(agents_dir, filename)
            rel_file_path = os.path.relpath(file_path, workspace_dir)
            total_checked += 1
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for absolute paths
                if abs_path_re.search(content):
                    errors.append({
                        'file': rel_file_path,
                        'type': 'absolute_path_detected',
                        'reason': 'พบพาธระบบแบบ Absolute (เช่น /Users/ หรือ /home/) กรุณาเปลี่ยนเป็น Relative Path เพื่อรองรับการทำงานร่วมกัน'
                    })
                
                # Check for secrets
                secret_errors = scan_for_secrets(content, rel_file_path)
                errors.extend(secret_errors)
                
                # Check relative links to skill files
                links = skill_link_re.findall(content)
                for link in links:
                    if link.startswith('http') or link.startswith('#'):
                        continue
                    if link.startswith('file://') and not link.startswith('file:///'):
                        clean_path = link.replace('file://', '')
                        target_abs_path = os.path.abspath(os.path.join(workspace_dir, clean_path))
                    elif link.startswith('file:///'):
                        continue
                    else:
                        target_abs_path = os.path.abspath(os.path.join(os.path.dirname(file_path), link))
                        
                    if '.agents/skills/' in target_abs_path or '.agents/AGENTS.md' in target_abs_path or 'second-brain/' in target_abs_path:
                        if not os.path.exists(target_abs_path):
                            errors.append({
                                'file': rel_file_path,
                                'type': 'broken_relative_link',
                                'reason': f'ลิงก์สัมพัทธ์ชี้ไปยังเป้าหมายที่ไม่มีจริง: {link} (พาธจริงที่หา: {os.path.relpath(target_abs_path, workspace_dir)})'
                            })
            except Exception as e:
                errors.append({
                    'file': rel_file_path,
                    'type': 'read_error',
                    'reason': f'ไม่สามารถอ่านไฟล์เพื่อตรวจสอบได้: {e}'
                })
    return total_checked, errors

def check_workspace_rules(workspace_dir):
    """ตรวจสอบไฟล์กฎของโปรเจกต์ .agents/AGENTS.md"""
    errors = []
    agents_md = os.path.join(workspace_dir, '.agents', 'AGENTS.md')
    if not os.path.exists(agents_md):
        return errors
        
    rel_file_path = os.path.relpath(agents_md, workspace_dir)
    abs_path_re = re.compile(r'(?:file:///Users/|/Users/|file:///home/|/home/)(?!username\b)')
    
    try:
        with open(agents_md, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if abs_path_re.search(content):
            errors.append({
                'file': rel_file_path,
                'type': 'absolute_path_detected',
                'reason': 'พบพาธระบบแบบ Absolute (เช่น /Users/ หรือ /home/) กรุณาเปลี่ยนเป็น Relative Path เพื่อรองรับการทำงานร่วมกัน'
            })
            
        # Check for secrets
        secret_errors = scan_for_secrets(content, rel_file_path)
        errors.extend(secret_errors)
    except Exception as e:
        errors.append({
            'file': rel_file_path,
            'type': 'read_error',
            'reason': f'ไม่สามารถอ่านไฟล์ตรวจสอบ AGENTS.md ได้: {e}'
        })
        
    return errors

def check_strategy_b_folders(workspace_dir):
    """ตรวจสอบความสมบูรณ์ของโฟลเดอร์ฟีเจอร์ตาม Strategy B"""
    errors = []
    features_dir = os.path.join(workspace_dir, 'second-brain', '10-requirements-spec', 'features')
    if not os.path.exists(features_dir):
        return errors
        
    for slug in os.listdir(features_dir):
        slug_dir = os.path.join(features_dir, slug)
        if os.path.isdir(slug_dir):
            # Check for required files
            required_files = ['brd.md', 'epics_user_stories.md', 'system_spec.md']
            for req_file in required_files:
                file_path = os.path.join(slug_dir, req_file)
                if not os.path.exists(file_path):
                    rel_path = os.path.relpath(file_path, workspace_dir)
                    errors.append({
                        'file': rel_path,
                        'type': 'missing_feature_artifact',
                        'reason': f"ฟีเจอร์ '{slug}' ขาดไฟล์สเปกที่จำเป็น: {req_file} (กลยุทธ์ B บังคับให้มี BRD, Epics & User Stories, และ System Spec ในทุกๆ ฟีเจอร์)"
                    })
    return errors

def sync_gitnexus_agents(workspace_dir):
    """ซิงค์ข้อมูล GitNexus จาก AGENTS.md (Root) ไปยัง .agents/AGENTS.md แบบอัตโนมัติ"""
    root_agents = os.path.join(workspace_dir, 'AGENTS.md')
    target_agents = os.path.join(workspace_dir, '.agents', 'AGENTS.md')
    
    if not os.path.exists(root_agents) or not os.path.exists(target_agents):
        return
        
    try:
        with open(root_agents, 'r', encoding='utf-8') as f:
            root_content = f.read()
            
        start_tag = '<!-- gitnexus:start -->'
        end_tag = '<!-- gitnexus:end -->'
        
        if start_tag not in root_content or end_tag not in root_content:
            return
            
        start_idx = root_content.find(start_tag)
        end_idx = root_content.find(end_tag) + len(end_tag)
        gitnexus_block = root_content[start_idx:end_idx]
        
        with open(target_agents, 'r', encoding='utf-8') as f:
            target_content = f.read()
            
        if start_tag in target_content and end_tag in target_content:
            t_start_idx = target_content.find(start_tag)
            t_end_idx = target_content.find(end_tag) + len(end_tag)
            new_content = target_content[:t_start_idx] + gitnexus_block + target_content[t_end_idx:]
        else:
            header = "\n\n## 🤖 12. GitNexus — Code Intelligence\n\n"
            new_content = target_content.rstrip() + header + gitnexus_block + "\n"
            
        if new_content != target_content:
            with open(target_agents, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("🔄 Auto-synced GitNexus block from root AGENTS.md to .agents/AGENTS.md")
    except Exception as e:
        print(f"Warning: Error syncing GitNexus block: {e}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_dir = os.path.abspath(os.path.join(script_dir, '..'))
    root_dir = os.path.join(workspace_dir, 'second-brain')
    
    if not os.path.exists(root_dir):
        print(f"Error: second-brain directory not found at {root_dir}")
        sys.exit(1)
        
    # Sync GitNexus before scanning
    sync_gitnexus_agents(workspace_dir)
        
    print(f"🧠 Scanning Workspace Linter in: {workspace_dir}")
    file_map, headings_map = build_index(root_dir, workspace_dir)
    print(f"Found {len(file_map)} markdown files in Second Brain.")
    
    all_errors = []
    
    # Check 1: Wikilinks & Secrets in Second Brain
    total_links, link_errors, linked_basenames = check_links(root_dir, file_map, headings_map)
    print(f"Scanned {total_links} wikilinks.")
    all_errors.extend(link_errors)
    
    # Check 1.5: Orphan Files
    orphan_errors = check_orphans(file_map, linked_basenames)
    print(f"Checked for orphan files in Second Brain.")
    all_errors.extend(orphan_errors)
    
    # Check 1.6: Critical Files & Templates
    critical_file_errors = check_critical_files(workspace_dir)
    print(f"Checked critical files and templates.")
    all_errors.extend(critical_file_errors)
    
    # Check 2: Frontmatter & Tags
    total_fm, fm_errors = check_frontmatter(root_dir, file_map)
    print(f"Checked {total_fm} files for frontmatter & tags.")
    all_errors.extend(fm_errors)

    # Check 2.5: Second Brain Absolute Paths
    sb_abs_errors = check_second_brain_absolute_paths(root_dir, file_map)
    print(f"Checked absolute paths in Second Brain files.")
    all_errors.extend(sb_abs_errors)

    # Check 2.6: Strategy B Folder Completeness
    strategy_b_errors = check_strategy_b_folders(workspace_dir)
    print(f"Checked Strategy B active feature folders.")
    all_errors.extend(strategy_b_errors)

    # Check 3: Agent configurations
    total_agents, agent_errors = check_agent_configurations(workspace_dir)
    print(f"Checked {total_agents} agent configurations in .agents/agents/.")
    all_errors.extend(agent_errors)

    # Check 4: Workspace rules (AGENTS.md)
    agents_md_errors = check_workspace_rules(workspace_dir)
    print(f"Checked .agents/AGENTS.md workspace rules.")
    all_errors.extend(agents_md_errors)
    
    if all_errors:
        print(f"\n❌ Linter detected {len(all_errors)} issue(s) in Workspace:\n")
        
        # Group and display errors
        for err in all_errors:
            print(f"  [{err['file']}] ({err['type']}):")
            print(f"    Reason: {err['reason']}\n")
        
        sys.exit(1)
    else:
        print("\n✅ All checks passed! Workspace integrity is completely healthy.")
        print("   - Second Brain Wikilinks: OK")
        print("   - Second Brain Frontmatter & Tags: OK")
        print("   - Second Brain (No absolute paths): OK")
        print("   - Second Brain (No orphan files): OK")
        print("   - Critical Files & Templates: OK")
        print("   - Secrets & Credentials Leak Scan: OK")
        print("   - Strategy B Feature Folders: OK")
        print("   - Agent Configs (No absolute paths & links valid): OK")
        print("   - AGENTS.md Workspace Rules (No absolute paths): OK")
        sys.exit(0)

if __name__ == '__main__':
    main()
