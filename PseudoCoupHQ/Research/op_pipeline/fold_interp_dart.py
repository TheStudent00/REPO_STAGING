#!/usr/bin/env python3
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
IN_FILE = os.path.join(HERE, "jit_out_dart", "all_opt.txt")
OUT_FILE = os.path.join(HERE, "op_dart.json")

def parse_dart_vm(txt):
    """Parse Dart VM output text to extract x64 instructions for each method."""
    lines = txt.split("\n")
    results = {}
    
    current_method = None
    current_asm = []
    current_bytes = []
    
    in_function = False
    
    for line in lines:
        # Match start of method
        # e.g. Code for function 'file:///.../program.dart_::_op_76' (RegularFunction) {
        match = re.search(r"Code for function 'file://.*_::_(op_\d+)'", line)
        if match:
            if current_method:
                results[current_method] = {
                    "ir_nodes": [], # FlowGraph IR can be extracted, but here we just get asm for now
                    "asm": current_asm,
                    "bytes": current_bytes
                }
            current_method = match.group(1)
            current_asm = []
            current_bytes = []
            in_function = True
            continue
            
        if not in_function:
            continue
            
        if line.startswith("}") and not line.startswith("} "):
            in_function = False
            continue
            
        if in_function:
            # Assembly lines look like: 0x7b16ba089d66    55                     push rbp
            # Or comments:        ;; Enter frame
            if line.strip() and line.startswith("0x"):
                parts = line.strip().split(maxsplit=2)
                if len(parts) >= 3:
                    byte_str = parts[1]
                    inst = parts[2]
                    
                    # byte_str is hex e.g. "55" or "4889e5"
                    hex_bytes = [byte_str[i:i+2] for i in range(0, len(byte_str), 2)]
                    current_bytes.extend(hex_bytes)
                    current_asm.append(inst)
            elif line.strip() and not line.strip().startswith(";;"):
                # some instructions don't have bytes or address? Unlikely in dart
                pass
                
    # Save last
    if current_method:
        results[current_method] = {
            "ir_nodes": [],
            "asm": current_asm,
            "bytes": current_bytes
        }
        
    return results

def main():
    if not os.path.exists(IN_FILE):
        print(f"Error: {IN_FILE} does not exist.")
        sys.exit(1)
            
    with open(IN_FILE) as f:
        results = parse_dart_vm(f.read())
            
    with open(OUT_FILE, "w") as f:
        json.dump(results, f, indent=2)
        
    print(f"Folded {len(results)} Dart probes into {OUT_FILE}")

if __name__ == "__main__":
    main()
