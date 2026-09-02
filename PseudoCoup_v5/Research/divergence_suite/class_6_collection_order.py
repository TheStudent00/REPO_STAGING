"""Class 6 — collection-order.

Naive divergence: iteration order of maps/sets reaching output.
  Python dict / Ruby / PHP / JS Map: insertion order.
  Go map: deliberately randomized EVERY RUN.
  Java HashMap / Rust HashMap / Swift: unspecified.
Same styled loop, different (or nondeterministic) output.

Policy fix (policy 6 + Table 3 P10/P11): PC.map and PC.set are
insertion-ordered on every target (LinkedHashMap-style polyfill where
the native map is unordered). Unordered maps are an explicit perf
borrow that forbids order-dependent output.
"""

m = {}
m["zebra"] = 1
m["apple"] = 2
m["mango"] = 3

print("keys   =", list(m.keys()))       # insertion order, all targets

s = ["zebra", "apple", "zebra", "mango"]
seen = {}                                # PC.set via insertion-ordered map
for item in s:
    seen[item] = True
print("dedup  =", list(seen.keys()))    # ['zebra', 'apple', 'mango']
