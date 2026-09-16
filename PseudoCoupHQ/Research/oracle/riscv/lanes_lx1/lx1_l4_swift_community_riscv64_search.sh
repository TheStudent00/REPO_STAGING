#!/bin/bash
# lx1_l4_swift_community_riscv64_search.sh -- task lx1, lane 4: the
# second half of the brief's question 1 -- "does a community toolchain
# exist (a riscv64 Linux build of the compiler itself)?" -- asked of
# GitHub's own search API (allow-listed: `.github.com`), by name, and
# recorded LITERAL. This is the last network lane of task lx1; every
# lane after this one runs with no route out.
set -u
total=2

i=1
echo "[$i/$total] GitHub repository search: swift + riscv64 (by name/description)"
for q in "swift riscv64" "swift-riscv64 toolchain" "swiftc riscv64"; do
  echo "  -- query: $q --"
  curl -fsSL --max-time 30 -H "Accept: application/vnd.github+json" \
    "https://api.github.com/search/repositories?q=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$q")&per_page=10" \
    -o /tmp/lx1_gh_search.json
  echo "    exit: $?"
  python3 -c "
import json
try:
    doc = json.load(open('/tmp/lx1_gh_search.json'))
except Exception as e:
    print('    could not parse:', e)
    raise SystemExit
if 'items' not in doc:
    print('    no items key; raw message:', doc.get('message'))
else:
    print('    total_count:', doc.get('total_count'))
    for item in doc['items'][:10]:
        print('    -', item['full_name'], '--', (item.get('description') or '')[:100])
"
done

i=2
echo ""
echo "[$i/$total] GitHub code search: 'riscv64-unknown-linux-gnu' inside files mentioning swift-sdk.json shape (best-effort; the code search API needs auth for most queries and this records what an unauthenticated call gets)"
curl -fsSL --max-time 30 -H "Accept: application/vnd.github+json" \
  "https://api.github.com/search/code?q=riscv64+swift-sdk.json" \
  -o /tmp/lx1_gh_code_search.json
echo "  exit: $?"
cat /tmp/lx1_gh_code_search.json
echo ""

python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
