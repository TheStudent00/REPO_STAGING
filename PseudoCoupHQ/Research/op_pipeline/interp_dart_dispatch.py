#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import re

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "probe_manifest_dart.json")

def run_dart():
    with open(MANIFEST) as f:
        doc = json.load(f)
    
    probes = doc["probes"]
    
    out_dir = os.path.join(HERE, "jit_out_dart")
    os.makedirs(out_dir, exist_ok=True)
    
    program_dart = os.path.join(out_dir, "program.dart")
    
    def get_dummy(t):
        if t == "bool": return "true"
        if t == "double": return "1.0"
        return "1"

    # Start with all probes active
    active_probes = set(probes.keys())
    
    while True:
        lines = []
        # We need to track the line numbers of each probe so we can remove them if they error
        probe_lines = {}
        
        for n in active_probes:
            p = probes[n]
            start_line = len(lines) + 1
            src_lines = p["source"].replace("public static", "").split("\n")
            for sl in src_lines:
                if sl.strip():
                    lines.append(sl.strip())
            end_line = len(lines)
            probe_lines[n] = (start_line, end_line)
            
        lines.append("void main() {")
        lines.append("  for (int i = 0; i < 3; i++) {")
        for n in active_probes:
            p = probes[n]
            sym = p["symbol"]
            lt = get_dummy(p["lhs_type"])
            if p["arity"] == "unary":
                lines.append(f"    try {{ {sym}({lt}); }} catch (e) {{}}")
            else:
                rt = get_dummy(p.get("rhs_type"))
                lines.append(f"    try {{ {sym}({lt}, {rt}); }} catch (e) {{}}")
        lines.append("  }")
        lines.append("}")
        
        with open(program_dart, "w") as f:
            f.write("\n".join(lines))
            
        print(f"Building Dart project with {len(active_probes)} probes...")
        res = subprocess.run(["dart", "compile", "exe", program_dart], capture_output=True, text=True)
        
        if res.returncode == 0:
            print("Compile succeeded!")
            break
            
        # Parse dart compile output
        error_lines = set()
        for line in res.stdout.split("\n") + res.stderr.split("\n"):
            match = re.search(r"program\.dart:(\d+):", line)
            if match and "Error" in line:
                error_lines.add(int(match.group(1)))
                
        to_remove = set()
        for err_line in error_lines:
            for n, (start, end) in probe_lines.items():
                if start <= err_line <= end:
                    to_remove.add(n)
        
        if not to_remove:
            if "Error" not in res.stdout and "Error" not in res.stderr:
                print("No errors found. Proceeding.")
                break
            print("Error: Could not identify which probes caused the compilation error.")
            print(res.stdout)
            sys.exit(1)
            
        print(f"Removing {len(to_remove)} invalid probes...")
        for n in to_remove:
            active_probes.remove(n)

    print("Running Dart project with FlowGraph Dump...")
    # --optimization-counter-threshold=1 to aggressively JIT
    res = subprocess.run(
        ["dart", "--optimization-counter-threshold=1", "--print-flow-graph-optimized", "--disassemble", program_dart], 
        capture_output=True,
        text=True
    )
    
    with open(os.path.join(out_dir, "all_opt.txt"), "w") as f:
        f.write(res.stdout)
        f.write(res.stderr)
        
    print("Done writing to all_opt.txt")

if __name__ == "__main__":
    run_dart()
