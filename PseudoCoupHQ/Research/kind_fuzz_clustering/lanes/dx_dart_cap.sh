#!/bin/sh
# log 030 -- does `dart analyze <dir>` cap the number of diagnostics it
# reports?  500 files, EVERY ONE of them a guaranteed NON_BOOL_OPERAND
# error.  If fewer than 500 distinct files come back with an ERROR then
# the harness's "no diagnostic means ACCEPT" rule silently accepts the
# remainder, and every chunked dart verdict is suspect.
set -u
export HOME=/work
export PATH=/persist/dart-sdk/bin:$PATH
R=/work/dx_dart_cap
for N in 100 300 500 1000; do
  rm -rf "$R"; mkdir -p "$R"
  i=0
  while [ $i -lt $N ]; do
    i=$((i+1))
    printf 'void p%s() {\n  Map<String, int> a = {};\n  String b = "hello";\n  var _r = (a) && (b);\n  print(_r);\n}\n' "$i" > "$R/T$i.dart"
  done
  D=$( cd "$R" && dart analyze --format=machine . 2>&1 )
  F=$( echo "$D" | grep '^ERROR' | awk -F'|' '{print $4}' | sort -u | wc -l )
  T=$( echo "$D" | grep -cE '^(ERROR|WARNING|INFO)' )
  echo "files=$N  distinct files with an ERROR=$F  total diagnostics=$T"
done > /out/dx_dart_cap.txt 2>&1
echo "__SUMMARY__|4|4|0|0" >> /out/dx_dart_cap.txt
rm -rf "$R"
echo "=== dx_dart_cap done ==="
