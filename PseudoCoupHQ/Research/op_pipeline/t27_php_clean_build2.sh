#!/bin/bash
# Task 27, second attempt at a clean php pair. The first attempt
# (t27_php_clean_build.sh) got past the libxml-2.0 wall for the first time
# -- configure exit=0 with every bundled extension disabled -- and then
# stopped in make with:
#   ext/standard/scanf.c:1044:62: error: too many arguments to function
#   'fn'; expected 0, have 3
# which is this container's gcc defaulting to a newer C standard in which
# an empty parameter list means "no parameters". The fix is a language
# standard flag, -std=gnu17; it changes no code.
# Also dumps ruby's rb_fix_plus_fix, the symbol fix_plus actually calls.
set -x
mkdir -p /out/t27

echo "[1/4] ruby: the computation symbol the anchor route calls"
for sym in rb_fix_plus_fix rb_int2big; do
  for tag in anchor ship; do
    b="/persist/ruby_${tag}/ruby"
    objdump -d --disassemble="$sym" "$b" > "/out/t27/ruby_${tag}_${sym}.txt" 2>&1
    echo "$sym $tag lines=$(wc -l < /out/t27/ruby_${tag}_${sym}.txt)"
    nm "$b" 2>/dev/null | grep -E " $sym$"
  done
done

echo "[2/4] php clean anchor: reconfigure with -std=gnu17, rebuild"
cd /persist/php_c_anchor
make clean > /persist/php_c_anchor_clean2.log 2>&1
./configure --disable-all --without-pear --disable-cgi \
  CFLAGS="-O0 -g -fwrapv -std=gnu17" > /persist/php_c_anchor_configure2.log 2>&1
echo "php clean anchor configure exit=$?"
make -j6 > /persist/php_c_anchor_make2.log 2>&1
echo "php clean anchor make exit=$?"
grep -n "error:" /persist/php_c_anchor_make2.log | head -5
ls -la /persist/php_c_anchor/sapi/cli/php 2>&1

echo "[3/4] php clean ship: same, optimizer on"
cd /persist/php_c_ship
make clean > /persist/php_c_ship_clean2.log 2>&1
./configure --disable-all --without-pear --disable-cgi \
  CFLAGS="-O2 -g -std=gnu17" > /persist/php_c_ship_configure2.log 2>&1
echo "php clean ship configure exit=$?"
make -j6 > /persist/php_c_ship_make2.log 2>&1
echo "php clean ship make exit=$?"
grep -n "error:" /persist/php_c_ship_make2.log | head -5
ls -la /persist/php_c_ship/sapi/cli/php 2>&1

echo "[4/4] contamination check, pin, raw dumps from whatever built"
for tag in anchor ship; do
  b="/persist/php_c_${tag}/sapi/cli/php"
  if [ -x "$b" ]; then
    echo "=== $b"
    md5sum "$b"
    echo "gcov symbols: $(nm "$b" 2>/dev/null | grep -c gcov)"
    "$b" -v 2>&1 | head -2
    nm "$b" 2>/dev/null | grep -E " (add_function|ZEND_ADD_[A-Z_]*HANDLER|fast_long_add_function)$" \
      > "/out/t27/phpclean_${tag}_nm.txt"
    cat "/out/t27/phpclean_${tag}_nm.txt"
    for sym in $(awk '{print $3}' "/out/t27/phpclean_${tag}_nm.txt"); do
      objdump -d --disassemble="$sym" "$b" > "/out/t27/phpclean_${tag}_${sym}.txt" 2>&1
      echo "$sym $tag lines=$(wc -l < /out/t27/phpclean_${tag}_${sym}.txt)"
    done
  else
    echo "NO CLEAN BINARY for $tag -- recorded as a refusal, nothing passed off"
  fi
done
echo DONE
