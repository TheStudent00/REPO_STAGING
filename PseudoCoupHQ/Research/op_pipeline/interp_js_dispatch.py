#!/usr/bin/env python3
import json
import os
import subprocess
import tempfile
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "probe_manifest_javascript.json")
V8_DEBUG = os.path.expanduser("~/.jsvu/bin/v8-debug")

if not os.path.exists(V8_DEBUG):
    print("Error: v8-debug not found at", V8_DEBUG)
    sys.exit(1)

def run_v8():
    with open(MANIFEST) as f:
        doc = json.load(f)
    
    probes = doc["probes"]
    
    out_dir = os.path.join(HERE, "jit_out_javascript")
    os.makedirs(out_dir, exist_ok=True)
    
    for n, p in probes.items():
        src = p["source"]
        sym = p["symbol"]
        
        # We write a warmup script that uses V8 native syntax to optimize the probe.
        # We pass arguments that match the type: number or boolean.
        
        if p["lhs_type"] == "boolean":
            lval = "true"
        else:
            lval = "1.0"
            
        if p.get("rhs_type") == "boolean":
            rval = "false"
        else:
            rval = "2.0"
            
        call_str = f"{sym}({lval})" if p["arity"] == "unary" else f"{sym}({lval}, {rval})"
        
        script = src + "\n"
        script += f"%PrepareFunctionForOptimization({sym});\n"
        script += f"{call_str};\n{call_str};\n"
        script += f"%OptimizeFunctionOnNextCall({sym});\n"
        script += f"{call_str};\n"
        
        js_file = os.path.join(out_dir, f"probe_{n}.js")
        with open(js_file, "w") as f:
            f.write(script)
        
        print(f"Running V8 on probe {n}...")
        try:
            # We run v8-debug and capture its output
            # --trace-turbo-path specifies where to dump the turbo*.json file
            res = subprocess.run(
                [V8_DEBUG, "--trace-turbo", f"--trace-turbo-path={out_dir}", "--print-opt-code", "--allow-natives-syntax", js_file],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            with open(os.path.join(out_dir, f"probe_{n}_opt.txt"), "w") as f:
                f.write(res.stdout)
                f.write(res.stderr)
                
        except subprocess.TimeoutExpired:
            print(f"Timeout on probe {n}")

if __name__ == "__main__":
    run_v8()
