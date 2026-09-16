#!/bin/bash
# lx1_l1_swift_riscv64_install_probe.sh -- task lx1, lane 1: with the
# NETWORK ON (this instance's one lane authorised for it, lx1.conf
# `proxy = yes`), does swift.org publish a Swift SDK for
# riscv64-unknown-linux-gnu for a 6.x release, or does a community
# riscv64 Linux build of the compiler itself exist?  Every command and
# its raw output is printed; nothing here is a guess.
#
# log_269 (task bb2, deliverable 5) already measured the NO-NETWORK
# state: swiftc accepts the riscv64 triple and prints a runtime path
# that does not exist; `swift sdk list` fails for a missing
# libxml2.so.2; the instance had `proxy = no`.  This lane repeats
# nothing already answered -- it installs libxml2 (the one thing that
# blocked `swift sdk list` from answering at all) and then asks the
# network the two questions the brief poses.
#
# Node: hq.research.arch_unit_oracle.riscv64.language_axis
# Brief: Research/briefs/task_lx1_brief.md, section 1
set -u

SWIFT=/persist/swift/usr/bin
total=6

i=1
echo "[$i/$total] libxml2, the one thing that blocked swift sdk list"
apt-get update 2>&1 | tail -5
echo "  exit: ${PIPESTATUS[0]}"
apt-get install -y libxml2 2>&1 | tail -20
echo "  exit: ${PIPESTATUS[0]}"

i=2
echo ""
echo "[$i/$total] \$ $SWIFT/swift sdk list"
"$SWIFT/swift" sdk list
echo "  exit: $?"

i=3
echo ""
echo "[$i/$total] \$ $SWIFT/swift sdk list --help (what the command that would install one wants)"
"$SWIFT/swift" sdk install --help 2>&1
echo "  exit: $?"

i=4
echo ""
echo "[$i/$total] does swift.org's own release JSON name riscv64 anywhere"
echo "  \$ curl -fsSL https://www.swift.org/api/v1/install/releases.json"
curl -fsSL --max-time 30 https://www.swift.org/api/v1/install/releases.json -o /tmp/lx1_releases.json
echo "  exit: $?"
if [ -f /tmp/lx1_releases.json ]; then
  echo "  bytes: $(wc -c < /tmp/lx1_releases.json)"
  echo "  grep -io riscv64:"
  grep -io "riscv64" /tmp/lx1_releases.json | sort -u
  echo "  (count: $(grep -io "riscv64" /tmp/lx1_releases.json | wc -l))"
  echo "  platforms this file names (grep -o '\"platform\":[^,]*' | sort -u):"
  grep -o '"platform"[^,}]*' /tmp/lx1_releases.json | sort -u
fi

i=5
echo ""
echo "[$i/$total] the known official cross-compile SDK bundle -- swiftlang/swift-static-linux-sdk releases, by name"
echo "  \$ curl -fsSL https://api.github.com/repos/swiftlang/swift-static-linux-sdk/releases"
curl -fsSL --max-time 30 -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/swiftlang/swift-static-linux-sdk/releases -o /tmp/lx1_sdk_releases.json
echo "  exit: $?"
if [ -f /tmp/lx1_sdk_releases.json ]; then
  echo "  bytes: $(wc -c < /tmp/lx1_sdk_releases.json)"
  echo "  grep -io riscv64 (count and unique lines):"
  grep -io "riscv64" /tmp/lx1_sdk_releases.json | sort -u
  echo "  (count: $(grep -io "riscv64" /tmp/lx1_sdk_releases.json | wc -l))"
  echo "  every asset name (\"name\":\"...\") this release list carries:"
  grep -o '"name": *"[^"]*"' /tmp/lx1_sdk_releases.json | sort -u
fi

i=6
echo ""
echo "[$i/$total] the toolchain download page's own platform list, riscv64 named or not"
echo "  \$ curl -fsSL https://www.swift.org/install/linux/"
curl -fsSL --max-time 30 https://www.swift.org/install/linux/ -o /tmp/lx1_install_linux.html
echo "  exit: $?"
if [ -f /tmp/lx1_install_linux.html ]; then
  echo "  bytes: $(wc -c < /tmp/lx1_install_linux.html)"
  echo "  grep -io riscv (count and unique lines):"
  grep -io "riscv[a-z0-9]*" /tmp/lx1_install_linux.html | sort -u
  echo "  (count: $(grep -io "riscv" /tmp/lx1_install_linux.html | wc -l))"
fi

python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
