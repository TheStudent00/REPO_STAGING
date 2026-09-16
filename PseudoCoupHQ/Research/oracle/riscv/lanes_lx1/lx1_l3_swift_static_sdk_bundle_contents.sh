#!/bin/bash
# lx1_l3_swift_static_sdk_bundle_contents.sh -- task lx1, lane 3: lane 2
# found download.swift.org DOES serve a "static-sdk" artifactbundle for
# swift-6.0.3-RELEASE (200 OK, 311056985 bytes) -- the one platform the
# release JSON names besides Linux/Windows/android-sdk/wasm-sdk. This
# lane downloads it (this instance's network-on lane) and reads its own
# manifest for which triples it carries, WITHOUT `swift sdk install`
# (still blocked: this image's libxml2 is soname 16
# (`libxml2-16`, `libxml2.so.16`, package `libxml2` itself has no
# installation candidate on Ubuntu resolute) and the `swift-sdk` helper
# in swift 6.0.3 wants `libxml2.so.2`, which no configured suite ships
# any more -- lane 2's own dpkg/apt-cache output).
set -u
total=4
URL="https://download.swift.org/swift-6.0.3-release/static-sdk/swift-6.0.3-RELEASE/swift-6.0.3-RELEASE_static-linux-0.0.1.artifactbundle.tar.gz"
OUT=/tmp/lx1_static_sdk.tar.gz

i=1
echo "[$i/$total] \$ curl -fSL $URL"
curl -fSL --max-time 600 "$URL" -o "$OUT"
echo "  exit: $?"
echo "  bytes on disk: $(wc -c < "$OUT" 2>/dev/null)"
echo "  sha256: $(sha256sum "$OUT" 2>/dev/null)"

i=2
echo ""
echo "[$i/$total] the archive's own top-level listing"
tar tzf "$OUT" 2>&1 | head -20
echo "  total entries: $(tar tzf "$OUT" 2>/dev/null | wc -l)"

i=3
echo ""
echo "[$i/$total] every path in the archive naming an architecture or a manifest"
tar tzf "$OUT" 2>/dev/null | grep -iE "riscv|x86_64|aarch64|arm64|info\.json|swift-sdk\.json" | sort -u

i=4
echo ""
echo "[$i/$total] the bundle's own info.json, LITERAL, wherever it sits"
INFO=$(tar tzf "$OUT" 2>/dev/null | grep -E "(^|/)info\.json$" | head -1)
echo "  info.json member: $INFO"
if [ -n "$INFO" ]; then
  mkdir -p /tmp/lx1_sdk_extract
  tar xzf "$OUT" -C /tmp/lx1_sdk_extract "$INFO"
  cat "/tmp/lx1_sdk_extract/$INFO"
fi
echo ""
echo "  every swift-sdk.json member, LITERAL:"
for member in $(tar tzf "$OUT" 2>/dev/null | grep -E "(^|/)swift-sdk\.json$"); do
  echo "  -- $member --"
  mkdir -p /tmp/lx1_sdk_extract
  tar xzf "$OUT" -C /tmp/lx1_sdk_extract "$member"
  cat "/tmp/lx1_sdk_extract/$member"
  echo ""
done

python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
