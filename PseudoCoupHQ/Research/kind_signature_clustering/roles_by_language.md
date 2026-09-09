# role vocabulary × language

Counts are how many KINDS in that grammar's node-types.json declare
the role; `—` = never declared. Generated from
`raw/<lang>.node-types.json`; regenerate with the snippet at the end.
NOTE: this file was linked in chat on 2026-08-12 before it existed —
written after the fact, same content as presented. The clustering
first pass (log_009) therefore inherited the 11-role list from
log_008 §4.3 instead (its decision 11); identical list.

| role | rust | python | kotlin | dart | c | cpp | languages |
|---|---|---|---|---|---|---|---|
| `alternative` | 2 | 4 | — | 3 | 6 | 6 | 5/6 |
| `arguments` | 2 | 1 | — | 2 | 1 | 5 | 5/6 |
| `body` | 16 | 13 | — | 11 | 12 | 18 | 5/6 |
| `condition` | 3 | 3 | — | 6 | 8 | 9 | 5/6 |
| `consequence` | 1 | 3 | — | 3 | 2 | 2 | 5/6 |
| `left` | 6 | 7 | — | 2 | 3 | 7 | 5/6 |
| `name` | 24 | 10 | — | 14 | 10 | 19 | 5/6 |
| `operator` | 2 | 4 | — | 2 | 6 | 10 | 5/6 |
| `parameters` | 4 | 2 | — | 3 | 3 | 7 | 5/6 |
| `right` | 5 | 7 | — | 2 | 3 | 8 | 5/6 |
| `value` | 14 | 9 | — | 3 | 12 | 14 | 5/6 |
| `argument` | 1 | 3 | — | — | 6 | 7 | 4/6 |
| `function` | 2 | 1 | — | — | 1 | 1 | 4/6 |
| `type` | 20 | 3 | — | — | 13 | 19 | 4/6 |
| `field` | 2 | — | — | — | 1 | 1 | 3/6 |
| `path` | 4 | — | — | — | 1 | 1 | 3/6 |
| `type_parameters` | 10 | 2 | — | 2 | — | — | 3/6 |
| `update` | — | — | — | 1 | 1 | 1 | 3/6 |

(2/6 and 1/6 tails omitted here; the generator prints all rows.)

```
cd PseudoCoupHQ/Research/kind_signature_clustering/raw && python3 - <<'PY'
import json, collections
langs = ["rust","python","kotlin","dart","c","cpp"]
roles = {L: collections.Counter(
    r for e in json.load(open(f"{L}.node-types.json"))
    for r in (e.get("fields") or {})) for L in langs}
allr = sorted(set().union(*map(set, roles.values())),
              key=lambda r: (-sum(r in roles[L] for L in langs), r))
print("| role | " + " | ".join(langs) + " | languages |")
print("|---"*8 + "|")
for r in allr:
    row = [str(roles[L][r]) if r in roles[L] else "—" for L in langs]
    print(f"| `{r}` | " + " | ".join(row)
          + f" | {sum(r in roles[L] for L in langs)}/6 |")
PY
```
