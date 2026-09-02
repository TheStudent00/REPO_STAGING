#!/usr/bin/env python3
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
IN_DIR = os.path.join(HERE, "jit_out_javascript")
OUT_FILE = os.path.join(HERE, "op_js.json")

def parse_asm(txt):
    """Parse V8 optimized code text to extract x64 instructions."""
    lines = txt.split("\n")
    asm = []
    bytes_arr = []
    in_instructions = False
    for line in lines:
        if line.startswith("Instructions (size = "):
            in_instructions = True
            continue
        if in_instructions:
            if not line.strip():
                break
            # V8 output format: 0x... offset bytes instruction
            # 0x79fdc280004c     c  ba92000000           movl rdx,0x92
            parts = line.strip().split(maxsplit=3)
            if len(parts) >= 4 and parts[0].startswith("0x"):
                byte_str = parts[2]
                inst = parts[3]
                
                # Split ba92000000 into ['ba', '92', '00', '00', '00']
                hex_bytes = [byte_str[i:i+2] for i in range(0, len(byte_str), 2)]
                bytes_arr.extend(hex_bytes)
                
                asm.append(inst)
    return asm, bytes_arr

def parse_turbo_json(path):
    """Parse TurboFan graph JSON to extract IR nodes."""
    try:
        with open(path) as f:
            data = json.load(f)
    except Exception:
        return []
    
    phases = data.get("phases", [])
    if not phases: return []
    
    # Get the last phase's nodes (usually code generation or late optimization)
    last_phase = phases[-1]
    nodes = last_phase.get("nodes", [])
    
    ir_nodes = []
    for node in nodes:
        op = node.get("title", "Unknown")
        ir_nodes.append(op)
    
    return ir_nodes

def main():
    if not os.path.exists(IN_DIR):
        print(f"Error: {IN_DIR} does not exist.")
        sys.exit(1)
        
    results = {}
    
    for fname in os.listdir(IN_DIR):
        if fname.endswith("_opt.txt"):
            base = fname.replace("_opt.txt", "")
            probe_name = base.replace("probe_", "op_")
            
            # Read ASM
            with open(os.path.join(IN_DIR, fname)) as f:
                asm, bytes_arr = parse_asm(f.read())
                
            # Read Turbo JSON
            # V8 generates turbo-op_X-0.json or turbo-<probe_name>-0.json
            # wait, the generated files are turbo-op_0-0.json (if name is op_0)
            turbo_file = os.path.join(IN_DIR, f"turbo-{probe_name}-0.json")
            if not os.path.exists(turbo_file):
                # Try fallback names
                turbo_file = os.path.join(IN_DIR, f"turbo-{base}-0.json")
                
            ir_nodes = parse_turbo_json(turbo_file) if os.path.exists(turbo_file) else []
            
            results[probe_name] = {
                "ir_nodes": ir_nodes,
                "asm": asm,
                "bytes": bytes_arr
            }
            
    with open(OUT_FILE, "w") as f:
        json.dump(results, f, indent=2)
        
    print(f"Folded {len(results)} JS probes into {OUT_FILE}")

if __name__ == "__main__":
    main()
