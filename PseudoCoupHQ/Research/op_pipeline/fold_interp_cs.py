#!/usr/bin/env python3
import json
import os
import re
import sys
from keystone import Ks, KS_ARCH_X86, KS_MODE_64

HERE = os.path.dirname(os.path.abspath(__file__))
IN_FILE = os.path.join(HERE, "jit_out_csharp", "all_opt.txt")
OUT_FILE = os.path.join(HERE, "op_cs.json")

def parse_ryujit(txt):
    """Parse CoreCLR RyuJIT output text to extract x64 instructions for each method."""
    lines = txt.split("\n")
    results = {}
    
    try:
        ks = Ks(KS_ARCH_X86, KS_MODE_64)
    except Exception as e:
        print("Keystone error:", e)
        ks = None
    
    current_method = None
    current_asm = []
    current_bytes = []
    in_instructions = False
    
    for line in lines:
        # Match start of method
        # e.g. ; Assembly listing for method Program:op_638(float,ulong):bool (MinOpts)
        match = re.match(r"^;\s*Assembly listing for method Program:(op_\d+)", line)
        if match:
            # Save previous
            if current_method:
                results[current_method] = {
                    "ir_nodes": [], # CoreCLR DOTNET_JitDisasm doesn't expose IR nodes natively without DOTNET_JitDump
                    "asm": current_asm,
                    "bytes": current_bytes
                }
            current_method = match.group(1)
            current_asm = []
            current_bytes = []
            in_instructions = False
            continue
            
        if not current_method:
            continue
            
        if line.startswith("G_M000_IG01"):
            in_instructions = True
            
        if line.startswith("; Total bytes of code"):
            in_instructions = False
            
        if in_instructions:
            # Ignore empty lines and block headers
            if not line.strip() or re.match(r"^G_M\d+_IG\d+:", line):
                continue
            # Also ignore comments
            if line.strip().startswith(";"):
                continue
                
            inst = line.strip()
            # Clean up CoreCLR specific operands for keystone
            inst = re.sub(r"\[\(reloc\s+0x[0-9a-fA-F]+\)\]", "[0x0]", inst)
            
            if ks:
                try:
                    encoding, count = ks.asm(inst)
                    if encoding:
                        hex_bytes = [f"{b:02x}" for b in encoding]
                        current_bytes.extend(hex_bytes)
                        current_asm.append(inst) # only append if it succeeds
                except Exception:
                    # some instructions might fail in keystone
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
        results = parse_ryujit(f.read())
            
    with open(OUT_FILE, "w") as f:
        json.dump(results, f, indent=2)
        
    print(f"Folded {len(results)} C# probes into {OUT_FILE}")

if __name__ == "__main__":
    main()
