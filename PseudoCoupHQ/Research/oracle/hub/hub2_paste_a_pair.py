#!/usr/bin/env python3
"""hub2_paste_a_pair.py -- task hub2: print one PAIR composition and the
two bodies the gate compared, so the report quotes the object rather
than describing it.  It reads `measure2.json` and writes nothing."""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
document = json.load(open(os.path.join(HERE, "measure2.json")))
for row in document["results"]:
    if row.get("level") != "pair":
        continue
    if row["target"] != "c":
        continue
    if row.get("verdict") != "PROVED":
        continue
    print("the corpus go unit: %s" % row["unit"])
    print("the composed c function:")
    print(row["text"])
    print("body A, go's own: %s" % row.get("body_a_text"))
    print("body B, the composition: %s" % row.get("body_b_text"))
    print("the gate: %s" % (row.get("check") or {}).get("reason"))
    break
