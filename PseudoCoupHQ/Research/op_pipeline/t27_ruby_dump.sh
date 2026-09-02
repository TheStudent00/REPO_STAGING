#!/bin/bash
# Task 27 -- raw objdump text for the ruby handler route, anchor and ship,
# out of the pinned builds at /persist/ruby_anchor and /persist/ruby_ship.
# No build is attempted here: both binaries already exist (checked before
# submitting this lane).
set -x
mkdir -p /out/t27

echo "[1/4] pin + contamination check (round-2 php lesson: a gcov-instrumented build is recorded as such)"
for tag in anchor ship; do
  b="/persist/ruby_${tag}/ruby"
  echo "=== $b"
  ls -la "$b"
  md5sum "$b"
  nm "$b" 2>/dev/null | grep -c gcov
  "$b" -v 2>&1 | head -1
done

echo "[2/4] symbol load addresses from nm"
for tag in anchor ship; do
  b="/persist/ruby_${tag}/ruby"
  nm "$b" 2>/dev/null | grep -E " (vm_opt_plus|rb_fix_plus|rb_int_plus|rb_big_plus|fix_plus)$" \
    > "/out/t27/ruby_${tag}_nm.txt"
  cat "/out/t27/ruby_${tag}_nm.txt"
done

echo "[3/4] raw objdump text per symbol, AT&T syntax, both builds"
for sym in vm_opt_plus rb_fix_plus rb_int_plus rb_big_plus fix_plus; do
  for tag in anchor ship; do
    b="/persist/ruby_${tag}/ruby"
    objdump -d --disassemble="$sym" "$b" > "/out/t27/ruby_${tag}_${sym}.txt" 2>&1
    echo "$sym $tag lines=$(wc -l < /out/t27/ruby_${tag}_${sym}.txt)"
  done
done

echo "[4/4] head of one dump, for the record"
head -20 /out/t27/ruby_anchor_rb_fix_plus.txt
echo DONE
