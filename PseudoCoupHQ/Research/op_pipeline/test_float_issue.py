import sys
sys.path.insert(0, "~/Programming/PseudoCoupHQ/Research/kind_fuzz_clustering")
sys.path.insert(0, "~/Programming/PseudoCoupHQ/Research/op_pipeline")
import arch_sem as AS
import sem_anchored as SA
import json

doc = SA.load("javascript")
for n, probe in doc["probes"].items():
    ship = probe.get("ship")
    if not ship: continue
    
    # Run the raw summarize to see if it throws
    try:
        AS.semantics(dict(state="OK", bytes=ship["bytes"], mnem=ship["mnem"], layout=SA.layout(ship)[0]))
    except TypeError as e:
        if 'float' in str(e):
            print(f"Probe {n} failed with float error:")
            print(f"  mnem: {ship['mnem']}")
            print(f"  expression: {probe['meta']['expression']}")
            break
