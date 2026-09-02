#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import re

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "probe_manifest_csharp.json")

def run_cs():
    with open(MANIFEST) as f:
        doc = json.load(f)
    
    probes = doc["probes"]
    
    out_dir = os.path.join(HERE, "jit_out_csharp")
    os.makedirs(out_dir, exist_ok=True)
    
    cs_dir = os.path.join(out_dir, "csproject")
    os.makedirs(cs_dir, exist_ok=True)
    
    if not os.path.exists(os.path.join(cs_dir, "csproject.csproj")):
        subprocess.run(["dotnet", "new", "console", "--force"], cwd=cs_dir, check=True)
    
    program_cs = os.path.join(cs_dir, "Program.cs")
    
    def get_dummy(t):
        if t == "bool": return "true"
        if t == "float": return "1.0f"
        if t == "double": return "1.0d"
        if t == "long": return "1L"
        if t == "ulong": return "1UL"
        return "1"

    # Start with all probes active
    active_probes = set(probes.keys())
    
    while True:
        lines = ["using System;"]
        lines.append("class Program {")
        lines.append("    static void Main() {")
        
        for n in active_probes:
            p = probes[n]
            sym = p["symbol"]
            lt = get_dummy(p["lhs_type"])
            if p["arity"] == "unary":
                lines.append(f"        try {{ {sym}({lt}); }} catch {{}}")
            else:
                rt = get_dummy(p.get("rhs_type"))
                lines.append(f"        try {{ {sym}({lt}, {rt}); }} catch {{}}")
                
        lines.append("    }")
        
        # We need to track the line numbers of each probe so we can remove them if they error
        probe_lines = {}
        
        for n in active_probes:
            p = probes[n]
            lines.append("    [System.Runtime.CompilerServices.MethodImpl(System.Runtime.CompilerServices.MethodImplOptions.NoInlining)]")
            
            start_line = len(lines) + 1
            src_lines = p["source"].replace("public static", "static").split("\n")
            for sl in src_lines:
                if sl.strip():
                    lines.append(sl)
            end_line = len(lines)
            probe_lines[n] = (start_line, end_line)
            
        lines.append("}")
        
        with open(program_cs, "w") as f:
            f.write("\n".join(lines))
            
        print(f"Building C# project with {len(active_probes)} probes...")
        res = subprocess.run(["dotnet", "build"], cwd=cs_dir, capture_output=True, text=True)
        
        if res.returncode == 0:
            print("Build succeeded!")
            break
            
        # Parse errors
        error_lines = set()
        for line in res.stdout.split("\n"):
            if "error CS" in line and "Program.cs(" in line:
                # format: Program.cs(45,12): error CS...
                match = re.search(r"Program\.cs\((\d+),", line)
                if match:
                    error_lines.add(int(match.group(1)))
                    
        to_remove = set()
        for err_line in error_lines:
            for n, (start, end) in probe_lines.items():
                if start <= err_line <= end:
                    to_remove.add(n)
                    
        if not to_remove:
            print("Error: Could not identify which probes caused the compilation error.")
            print(res.stdout)
            sys.exit(1)
            
        print(f"Removing {len(to_remove)} invalid probes...")
        for n in to_remove:
            active_probes.remove(n)

    print("Running C# project with DOTNET_JitDisasm...")
    env = os.environ.copy()
    env["DOTNET_JitDisasm"] = "*op_*"
    
    res = subprocess.run(
        ["dotnet", "bin/Debug/net8.0/csproject.dll"], 
        cwd=cs_dir, 
        env=env,
        capture_output=True,
        text=True
    )
    
    with open(os.path.join(out_dir, "all_opt.txt"), "w") as f:
        f.write(res.stdout)
        
    print("Done writing to all_opt.txt")

if __name__ == "__main__":
    run_cs()
