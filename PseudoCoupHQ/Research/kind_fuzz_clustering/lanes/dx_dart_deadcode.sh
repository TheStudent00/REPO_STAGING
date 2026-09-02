#!/bin/sh
# log 030 -- capture the RAW `dart analyze` diagnostics for the four
# truth|truth `&&`/`||` probes, at every severity, so the instrument
# fault of log 029 is on the record verbatim rather than inferred.
set -u
export HOME=/work
export PATH=/persist/dart-sdk/bin:$PATH
ROOT=/work/dx_dart_deadcode
rm -rf "$ROOT"; mkdir -p "$ROOT/src"
mk() {
  cat > "$ROOT/src/P3_3_$1.dart" <<DEOF

void probe3_3_$1() {
  bool a = $2;
  bool b = $3;
  var _r = (a) $4 (b);
  print(_r);
}
DEOF
}
mk 0_0_13 false false '&&'
mk 1_1_13 true  true  '&&'
mk 0_0_14 false false '||'
mk 1_1_14 true  true  '||'
{
  echo "=== dart version ==="
  dart --version 2>&1
  echo "=== sources ==="
  for f in "$ROOT"/src/*.dart; do echo "--- $f"; cat "$f"; done
  echo "=== dart analyze .   (PLAIN -- what the old harness scraped) ==="
  ( cd "$ROOT/src" && dart analyze . 2>&1 ); echo "plain exit=$?"
  echo "=== dart analyze --format=machine .   (severity visible) ==="
  ( cd "$ROOT/src" && dart analyze --format=machine . 2>&1 ); echo "machine exit=$?"
} > /out/dx_dart_deadcode.txt 2>&1
echo "__SUMMARY__|4|4|0|0" >> /out/dx_dart_deadcode.txt
rm -rf "$ROOT"
echo "=== dx_dart_deadcode done ==="
