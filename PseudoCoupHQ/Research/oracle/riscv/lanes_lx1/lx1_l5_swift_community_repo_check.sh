#!/bin/bash
# lx1_l5_swift_community_repo_check.sh -- task lx1, lane 5: lane 4's
# GitHub repository search returned exactly one hit for "swift
# riscv64" -- `mcritz/swift-riscv64`, described "Building swift for
# riscv64 platforms". This lane reads that repository's own releases
# and README, LITERAL, to say whether it PUBLISHES an installable
# riscv64 Linux build of the compiler or only describes building one.
# Last network lane of task lx1.
set -u
total=3

i=1
echo "[$i/$total] \$ curl .../repos/mcritz/swift-riscv64"
curl -fsSL --max-time 30 -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/mcritz/swift-riscv64" -o /tmp/lx1_repo.json
echo "  exit: $?"
cat /tmp/lx1_repo.json 2>/dev/null | python3 -c "
import json,sys
doc = json.load(sys.stdin)
for key in ('full_name','description','archived','fork','html_url','pushed_at','stargazers_count'):
    print(' ', key, '=', doc.get(key))
"

i=2
echo ""
echo "[$i/$total] \$ curl .../repos/mcritz/swift-riscv64/releases"
curl -fsSL --max-time 30 -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/mcritz/swift-riscv64/releases" -o /tmp/lx1_repo_releases.json
echo "  exit: $?"
echo "  bytes: $(wc -c < /tmp/lx1_repo_releases.json)"
cat /tmp/lx1_repo_releases.json

i=3
echo ""
echo "[$i/$total] \$ curl .../repos/mcritz/swift-riscv64/readme"
curl -fsSL --max-time 30 -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/mcritz/swift-riscv64/readme" -o /tmp/lx1_repo_readme.json
echo "  exit: $?"
python3 -c "
import json, base64
doc = json.load(open('/tmp/lx1_repo_readme.json'))
content = base64.b64decode(doc['content']).decode('utf-8', 'replace')
print(content[:3000])
"

python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
