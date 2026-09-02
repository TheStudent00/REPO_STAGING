# Divergence Suite

One runnable file per divergence class from
[../language_divergence_study_log.md](../../DevComms/language_divergence_study_log.md).

Each file:
- states the naive divergence (which target family computes what)
- states the policy that fixes it ([../PCv7_policy_decisions.md](../../Designing/PCv7_policy_decisions.md))
- prints the canonical output — the hub run IS the expected-results record

A class is proven implicit exactly when its file exists: identically
styled code, divergent naive outputs, convergent under policy.

## Files and expected output (hub run, 2026-07-24)

| File | Expected output |
|---|---|
| class_1_value_model.py | floor -4, trunc -3, wrap -9223372036854775808, bigint 9223372036854775808 |
| class_2_copy_model.py | alias 1, copy 0 |
| class_3_evaluation_order.py | order ['g','h'], result 3 |
| class_4_lifetime.py | open a, open b, work, close b, close a |
| class_5_dispatch.py | describe(x) = cat |
| class_6_collection_order.py | keys and dedup in insertion order |
| class_8_encoding.py | points 3 / 🙂, utf8 6, utf16 4 |

## Class 7 — deliberately absent

Concurrency was demoted from the divergence classes (study log,
"Class 7 final resolution"): transpiled with its service, outputs are
identical everywhere; only speed varies. No divergent script can be
written for it that respects the discipline (racy code is forbidden),
so it has no file — which is itself the demotion's proof restated.

## Use

Run all: `for f in class_*.py; do python3 "$f"; done`
Future: each egress target reruns the suite; a target passes when its
outputs match this table byte-for-byte.
