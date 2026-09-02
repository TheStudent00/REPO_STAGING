import json
import sys
import os

# Add pipeline directory to path so we can import the modules
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon12_normalize as C12N

def run_normalizer(json_path):
    with open(json_path, "r") as f:
        doc = json.load(f)

    units = doc.get("units", {})
    print(f"Normalizing {len(units)} interpreter units...")

    success_count = 0
    refused_count = 0

    for n, unit in units.items():
        raw_text = unit.get("derived_text")
        if not raw_text:
            continue
        
        # We assume canon4_units_interp derived_text is a single expression string or we join it
        # Actually in canon4 it's a string, so we pass it directly
        expr_text = raw_text
        
        norm, ok, note = C12N.normalize_v2(expr_text)
        
        if ok:
            success_count += 1
            print(f"[{n}] SUCCESS: {norm}")
        else:
            refused_count += 1
            print(f"[{n}] REFUSED: {note}")

    print(f"\nResults: {success_count} success, {refused_count} refused.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_normalizer(sys.argv[1])
    else:
        print("Usage: python test_normalizer.py <path_to_json>")
