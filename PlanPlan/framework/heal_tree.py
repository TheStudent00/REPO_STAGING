#!/usr/bin/env python3
"""
heal_tree.py - The "Hand-of-God" physical reconciler for PlanPlan.
Walks the planning tree top-down and forces all directories and files
to conform to the strict prefix chains, scaffolding missing node files,
and then calls generate_nodes.py to heal the YAML edges.
"""

import os
import argparse
import re
import sys
import subprocess
from datetime import date

# Skeletons for scaffolding raw folders
CORE_SKELETON = """\
---
id: {id}
level: {level}
status: draft
settled_by: {user}
supersedes: null
---

# CORE {chain} — {title}

## definition

*(pending — scaffolded by heal_tree.py on {today})*
"""

PROGRESS_SKELETON = """\
---
id: {id}.progress
status: living
---

# PROGRESS — {title}

- {today}: Scaffolded by `heal_tree.py`.
"""

CHECK_SKELETON = """\
---
id: {id}.check
---

# CHECK — {chain}_{title}

Node `{id}`. Status `draft`.

## check 1 — completeness

*(scaffolded)*
"""

def disp(path):
    home = os.path.expanduser("~")
    ap = os.path.abspath(path)
    return "~" + ap[len(home):] if ap.startswith(home + os.sep) else ap

def scaffold_node(dirpath, chain, title, parent_id=None, node_id=None):
    today = date.today().isoformat()
    level = chain.count("_")
    user = os.environ.get("USER", "Unknown")
    if not node_id:
        node_id = f"{parent_id}.{title}" if parent_id else title
    
    core_path = os.path.join(dirpath, f"CORE_{chain}_{title}.md")
    check_path = os.path.join(dirpath, f"CHECK_{chain}_{title}.md")
    prog_path = os.path.join(dirpath, "PROGRESS.md")
    
    with open(core_path, "w", encoding="utf-8") as f:
        f.write(CORE_SKELETON.format(id=node_id, level=level, user=user, chain=chain, title=title, today=today))
        
    with open(check_path, "w", encoding="utf-8") as f:
        f.write(CHECK_SKELETON.format(id=node_id, chain=chain, title=title))
        
    with open(prog_path, "w", encoding="utf-8") as f:
        f.write(PROGRESS_SKELETON.format(id=node_id, title=title, today=today))
        
    print(f"  [Scaffolded] {title} -> CORE_{chain}_{title}.md")
    return node_id

def get_id_from_core(dirpath):
    core_files = [f for f in os.listdir(dirpath) if f.startswith("CORE_") and f.endswith(".md")]
    if not core_files:
        return None
    core_path = os.path.join(dirpath, core_files[0])
    with open(core_path, "r", encoding="utf-8") as f:
        content = f.read()
    m = re.search(r"^id:\s*([^\s]+)", content, re.M)
    if m:
        return m.group(1)
    return None

def heal_dir(dirpath, curr_chain, parent_id):
    # Determine the definitive name from the directory itself
    folder_name = os.path.basename(dirpath)
    dir_name_match = re.match(r"^node_((?:\d+_)*\d+)_([a-z0-9_]+)$", folder_name)
    name = dir_name_match.group(2) if dir_name_match else os.path.basename(dirpath).lower()
    
    # 1. Ensure CORE and CHECK files in THIS directory match curr_chain and name
    core_files = [f for f in os.listdir(dirpath) if f.startswith("CORE_") and f.endswith(".md")]
    
    if len(core_files) > 0:
        old_core = core_files[0]
        # Match both CORE_0_0_tools.md and CORE_0.md
        m = re.match(r"^CORE_((?:\d+_)*\d+)(?:_([a-z0-9_]+))?\.md$", old_core)
        if m:
            old_chain = m.group(1)
            old_name = m.group(2)
            
            # If chain or name mismatch, rename!
            if old_chain != curr_chain or old_name != name:
                new_core = f"CORE_{curr_chain}_{name}.md"
                if old_core != new_core:
                    os.rename(os.path.join(dirpath, old_core), os.path.join(dirpath, new_core))
                    print(f"  [Renamed] {old_core} -> {new_core}")
                
                # rename CHECK files matching the old pattern
                for f in os.listdir(dirpath):
                    if f.startswith(f"CHECK_{old_chain}"):
                        ext = f.split(".")[-1]
                        new_check = f"CHECK_{curr_chain}_{name}.{ext}"
                        if f != new_check:
                            os.rename(os.path.join(dirpath, f), os.path.join(dirpath, new_check))
                            print(f"  [Renamed] {f} -> {new_check}")
    else:
        # Raw directory, needs scaffolding!
        if dir_name_match:
            scaffold_node(dirpath, curr_chain, name, parent_id=parent_id)
        else:
            pass

    # Read CORE to get this directory's ID
    this_id = get_id_from_core(dirpath) or (f"{parent_id}.{name}" if name else parent_id)
    
    # 2. Process Subdirectories
    subdirs = [d for d in os.listdir(dirpath) if os.path.isdir(os.path.join(dirpath, d)) and not d.startswith(".")]
    if not subdirs:
        return
        
    used_indices = set()
    non_conforming = []
    
    for d in subdirs:
        m = re.match(r"^node_((?:\d+_)*\d+)_([a-z0-9_]+)$", d)
        if m:
            chain = m.group(1)
            if chain.startswith(curr_chain + "_"):
                suffix = chain[len(curr_chain)+1:]
                if "_" not in suffix and suffix.isdigit():
                    idx = int(suffix)
                    if idx not in used_indices:
                        used_indices.add(idx)
                        continue
        non_conforming.append(d)
        
    max_idx = max(used_indices) if used_indices else -1
    
    non_conforming.sort()
    for d in non_conforming:
        max_idx += 1
        new_chain = f"{curr_chain}_{max_idx}"
        
        # Extract base name
        m = re.match(r"^node_((?:\d+_)*\d+)_([a-z0-9_]+)$", d)
        if m:
            base_name = m.group(2)
        else:
            base_name = d
            
        # sanitize base_name
        base_name = re.sub(r'[^a-z0-9_]', '_', base_name.lower()).strip('_')
        if not base_name:
            base_name = f"node_{max_idx}"
            
        new_name = f"node_{new_chain}_{base_name}"
        os.rename(os.path.join(dirpath, d), os.path.join(dirpath, new_name))
        print(f"  [Re-Indexed] {d}/ -> {new_name}/")
        
    # 3. Recurse
    # Re-list subdirectories because we renamed them
    subdirs = [d for d in os.listdir(dirpath) if os.path.isdir(os.path.join(dirpath, d)) and not d.startswith(".")]
    for d in subdirs:
        m = re.match(r"^node_((?:\d+_)*\d+)_([a-z0-9_]+)$", d)
        if m:
            chain = m.group(1)
            heal_dir(os.path.join(dirpath, d), chain, this_id)

def main():
    parser = argparse.ArgumentParser(description="Heal a dragged-and-dropped physical folder layout to conform to PlanPlan strict chain structure.")
    parser.add_argument("planning_root", help="Path to the planning root directory")
    args = parser.parse_args()
    
    root = os.path.abspath(args.planning_root)
    if not os.path.exists(root):
        print(f"Error: Directory '{root}' does not exist.")
        sys.exit(1)
        
    core_files = [f for f in os.listdir(root) if f.startswith("CORE_") and f.endswith(".md")]
    if not core_files:
        print(f"Scaffolding missing root CORE file at {root}...")
        root_name = os.path.basename(root).lower()
        root_chain = "0"
        scaffold_node(root, root_chain, root_name, node_id="root")
    else:
        root_core = core_files[0]
        m = re.match(r"^CORE_((?:\d+_)*\d+)(?:_.*)?\.md$", root_core)
        if not m:
            print(f"Error: Planning root CORE file '{root_core}' is invalid.")
            sys.exit(1)
            
        root_chain = m.group(1)
    
    print(f"=== 1. Physical Normalization ===")
    print(f"Healing tree at {disp(root)} (root chain: {root_chain})")
    
    root_id = get_id_from_core(root) or "0"
    heal_dir(root, root_chain, root_id)
    
    print(f"\n=== 2. YAML Healing ===")
    framework_dir = os.path.dirname(os.path.abspath(__file__))
    gen_nodes = os.path.join(framework_dir, "generate_nodes.py")
    
    gen_dash = os.path.join(framework_dir, "generate_dashboards.py")
    
    cmds = [
        ["python3", gen_nodes, root, "--adopt", "--apply"],
        ["python3", gen_nodes, root, "--adopt-edges", "--adopt-checks", "--apply"],
        ["python3", gen_nodes, root, "--projections", "--apply"],
        ["python3", gen_dash, root]
    ]
    
    for cmd in cmds:
        print(f"Running: {' '.join(cmd)}")
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {e}")
            sys.exit(1)
            
    print("\nHeal complete! Tree is fully reconciled.")

if __name__ == "__main__":
    main()
