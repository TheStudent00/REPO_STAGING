#!/usr/bin/env python3
"""
shift_node.py - Move a node and all of its sub-nodes into a new parent directory,
automatically renaming the folders and files to match the new hierarchical depth.
"""

import os
import shutil
import argparse
import re
import sys

def get_new_name(filename, old_chain, new_chain):
    """
    Given a filename (folder or file), return the renamed version
    with old_chain replaced by new_chain, or None if it shouldn't be renamed.
    """
    # Match node folders
    m = re.match(r"^node_((?:\d+_)*\d+)_([a-z0-9_]+)$", filename)
    if m:
        chain = m.group(1)
        name = m.group(2)
        if chain == old_chain or chain.startswith(old_chain + "_"):
            new_c = new_chain + chain[len(old_chain):]
            return f"node_{new_c}_{name}"
            
    # Match CORE or CHECK files with any extension
    m = re.match(r"^(CORE|CHECK)_((?:\d+_)*\d+)_([a-z0-9_]+)(\.[a-zA-Z0-9_]+)$", filename)
    if m:
        prefix = m.group(1)
        chain = m.group(2)
        name = m.group(3)
        ext = m.group(4)
        if chain == old_chain or chain.startswith(old_chain + "_"):
            new_c = new_chain + chain[len(old_chain):]
            return f"{prefix}_{new_c}_{name}{ext}"
            
    return None

def main():
    parser = argparse.ArgumentParser(description="Shift (re-home) a node and all of its sub-nodes into a new parent directory.")
    parser.add_argument("src", help="Path to the node to move")
    parser.add_argument("dst_parent", help="Path of the target parent node")
    
    args = parser.parse_args()
    
    src = os.path.abspath(args.src)
    dst_parent = os.path.abspath(args.dst_parent)
    
    if not os.path.exists(src):
        print(f"Error: Source path '{src}' does not exist.")
        sys.exit(1)
        
    if not os.path.exists(dst_parent):
        print(f"Error: Target parent '{dst_parent}' does not exist.")
        sys.exit(1)
        
    if dst_parent.startswith(src + os.sep) or dst_parent == src:
        print("Error: Cannot move a node into itself or its children.")
        sys.exit(1)
        
    src_name = os.path.basename(src)
    src_match = re.match(r"^node_((?:\d+_)*\d+)_([a-z0-9_]+)$", src_name)
    if not src_match:
        print(f"Error: Source '{src_name}' does not look like a node folder.")
        sys.exit(1)
    
    old_chain = src_match.group(1)
    
    dst_name = os.path.basename(dst_parent)
    dst_match = re.match(r"^node_((?:\d+_)*\d+)_([a-z0-9_]+)$", dst_name)
    if not dst_match:
        print(f"Error: Target parent '{dst_name}' does not look like a node folder.")
        sys.exit(1)
        
    parent_chain = dst_match.group(1)
    
    # Find max index for new chain by looking at direct children of the target parent
    max_idx = -1
    for child in os.listdir(dst_parent):
        child_path = os.path.join(dst_parent, child)
        if os.path.isdir(child_path):
            cm = re.match(r"^node_((?:\d+_)*\d+)_([a-z0-9_]+)$", child)
            if cm:
                child_chain = cm.group(1)
                if child_chain.startswith(parent_chain + "_"):
                    suffix = child_chain[len(parent_chain)+1:]
                    # Only consider direct children (no deeper underscores)
                    if "_" not in suffix and suffix.isdigit():
                        max_idx = max(max_idx, int(suffix))
                        
    new_chain = f"{parent_chain}_{max_idx + 1}"
    
    print(f"Moving node '{src_name}' into '{dst_parent}'")
    print(f"Old chain prefix: {old_chain}")
    print(f"New chain prefix: {new_chain}")
    print("Renaming recursively...")
    
    # Walk bottom-up so we rename innermost files and folders before their parents
    for dirpath, dirnames, filenames in os.walk(src, topdown=False):
        # 1. Rename files inside dirpath
        for fn in filenames:
            new_fn = get_new_name(fn, old_chain, new_chain)
            if new_fn and new_fn != fn:
                old_p = os.path.join(dirpath, fn)
                new_p = os.path.join(dirpath, new_fn)
                os.rename(old_p, new_p)
                
        # 2. Rename directories inside dirpath
        for dn in dirnames:
            new_dn = get_new_name(dn, old_chain, new_chain)
            if new_dn and new_dn != dn:
                old_p = os.path.join(dirpath, dn)
                new_p = os.path.join(dirpath, new_dn)
                os.rename(old_p, new_p)
                
    # 3. Move the root node itself
    new_src_name = get_new_name(src_name, old_chain, new_chain)
    if not new_src_name:
        new_src_name = src_name # fallback
        
    new_src_path = os.path.join(dst_parent, new_src_name)
    shutil.move(src, new_src_path)
    
    print(f"Done! Moved to: {new_src_path}")
    print("-" * 60)
    print("ACTION REQUIRED:")
    print("The YAML frontmatter has NOT been modified.")
    print("To heal the YAML frontmatter across the tree, run:")
    print("  python3 generate_nodes.py <planning_root> --adopt --apply")
    print("-" * 60)

if __name__ == "__main__":
    main()
