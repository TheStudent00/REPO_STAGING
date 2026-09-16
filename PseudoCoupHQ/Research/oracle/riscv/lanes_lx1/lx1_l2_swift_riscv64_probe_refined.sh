#!/bin/bash
# lx1_l2_swift_riscv64_probe_refined.sh -- task lx1, lane 2: lane 1
# found the release JSON names a "static-sdk" platform with ZERO
# "riscv64" hits and an apt install of libxml2 refused twice (a
# setgroups permission error, then "no installation candidate"). This
# lane reads what the static-sdk platform entry actually names, tries
# the Ubuntu package name a time_t-transitioned release gives libxml2,
# and asks apt directly what it has under that name -- so the "no
# candidate" finding is not left resting on one guessed package name.
set -u
total=4

i=1
echo "[$i/$total] the static-sdk platform entry, whole, from lane 1's own file"
curl -fsSL --max-time 30 https://www.swift.org/api/v1/install/releases.json -o /tmp/lx1_releases.json
echo "  exit: $?"
python3 -c "
import json
doc = json.load(open('/tmp/lx1_releases.json'))
def walk(node, path=''):
    if isinstance(node, dict):
        for k in node:
            walk(node[k], path + '/' + str(k))
    elif isinstance(node, list):
        for i, item in enumerate(node):
            walk(item, path + '[%d]' % i)
    else:
        text = str(node)
        if 'static-sdk' in path.lower() or 'static' in text.lower() or 'riscv' in text.lower():
            print(path, '=', text[:200])
"

i=2
echo ""
echo "[$i/$total] apt-cache policy / search for libxml2 under every name it might carry"
apt-cache policy libxml2 2>&1
echo "  ---"
apt-cache search libxml2 2>&1 | head -20
echo "  ---"
dpkg -l 'libxml2*' 2>&1
echo "  ---"
find / -xdev -iname 'libxml2.so*' 2>/dev/null

i=3
echo ""
echo "[$i/$total] apt sources this image actually has configured"
cat /etc/apt/sources.list 2>&1
ls /etc/apt/sources.list.d/ 2>&1
for f in /etc/apt/sources.list.d/*; do echo "-- $f --"; cat "$f" 2>&1; done

i=4
echo ""
echo "[$i/$total] the download.swift.org directory a static-sdk artifactbundle would sit under, for 6.0.3"
for url in \
  "https://download.swift.org/swift-6.0.3-release/static-sdk/swift-6.0.3-RELEASE/" \
  "https://download.swift.org/swift-6.0.3-release/static-sdk/swift-6.0.3-RELEASE/swift-6.0.3-RELEASE_static-linux-0.0.1.artifactbundle.tar.gz"
do
  echo "  \$ curl -fsSI --max-time 20 $url"
  curl -fsSI --max-time 20 "$url"
  echo "  exit: $?"
done

python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
