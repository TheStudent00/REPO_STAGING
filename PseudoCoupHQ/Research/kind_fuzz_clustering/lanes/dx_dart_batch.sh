#!/bin/sh
# log 030 -- is `dart analyze <dir>` on a 500-file chunk giving the same
# answer as `dart analyze` on the file alone?  The value matrix shows
# `Map && String` ACCEPT for some value pairs and REFUSE for others,
# which is not a rule any type checker could be following, so the
# suspicion is the BATCH and not the language.
set -u
export HOME=/work
export PATH=/persist/dart-sdk/bin:$PATH
R=/work/dx_dart_batch
rm -rf "$R"; mkdir -p "$R/solo" "$R/batch"
i=0
for k in empty emptykey flat intlike nested; do
  for v in base_empty base_hello base_lines clef eacute escapes; do
    i=$((i+1))
    cat > "$R/solo/T$i.dart" <<DEOF
void probe$i() {
  Map<String,int> a = <String,int>{};
  String b = "x";
  var _r = (a) && (b);
  print(_r);
}
DEOF
    cp "$R/solo/T$i.dart" "$R/batch/T$i.dart"
  done
done
N=$i
# pad the batch directory out to 500 files with trivially valid probes
j=$N
while [ $j -lt 500 ]; do
  j=$((j+1))
  printf 'void pad%s() {\n  int a = 1;\n  int b = 2;\n  var _r = (a) + (b);\n  print(_r);\n}\n' "$j" > "$R/batch/T$j.dart"
done
{
  echo "=== $N identical Map && String probes; solo dir has $N files, batch dir has 500 ==="
  echo "--- SOLO: dart analyze --format=machine on the $N-file dir"
  ( cd "$R/solo" && dart analyze --format=machine . 2>&1 ) | \
      awk -F'|' '{print $1"|"$3}' | sort | uniq -c | sort -rn
  echo "solo ERROR count: $( cd "$R/solo" && dart analyze --format=machine . 2>&1 | grep -c '^ERROR' )"
  echo "--- BATCH: same $N probes inside 500 files"
  echo "batch ERROR count on the T1..T$N probes: $( cd "$R/batch" && dart analyze --format=machine . 2>&1 | grep '^ERROR' | awk -F'|' '{print $4}' | sed 's#.*/##' | sed 's/\.dart//' | grep -E "^T([1-9]|[12][0-9]|30)$" | sort -u | wc -l )"
  echo "batch TOTAL diagnostics: $( cd "$R/batch" && dart analyze --format=machine . 2>&1 | grep -cE '^(ERROR|WARNING|INFO)' )"
  echo "--- which of T1..T$N are missing an ERROR in the batch run ---"
  ( cd "$R/batch" && dart analyze --format=machine . 2>&1 ) | grep '^ERROR' | \
      awk -F'|' '{print $4}' | sed 's#.*/##;s/\.dart//' | sort -u > "$R/haserr"
  k=1; miss=""
  while [ $k -le $N ]; do
    grep -qx "T$k" "$R/haserr" || miss="$miss T$k"
    k=$((k+1))
  done
  echo "missing:$miss"
} > /out/dx_dart_batch.txt 2>&1
echo "__SUMMARY__|500|500|0|0" >> /out/dx_dart_batch.txt
rm -rf "$R"
echo "=== dx_dart_batch done ==="
