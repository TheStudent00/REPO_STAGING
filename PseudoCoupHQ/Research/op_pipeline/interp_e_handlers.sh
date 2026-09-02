#!/bin/bash
set -x
echo "[1/12] grep ruby handler candidates"
grep -n "^vm_opt_plus\|^opt_plus\|vm_opt_plus(" /persist/ruby-3.3.0/vm_insnhelper.c | head -5
grep -n "^rb_fix_plus\|^fix_plus\|^static VALUE\s*$" /persist/ruby-3.3.0/numeric.c | grep -i plus
grep -n "rb_int_plus\|fix_plus" /persist/ruby-3.3.0/numeric.c | head -10
grep -n "^rb_big_plus\|bignum.c:.*plus" /persist/ruby-3.3.0/bignum.c | grep -i plus | head -10

echo "[2/12] grep php handler candidates"
grep -n "^ZEND_API.*add_function\|^add_function" /persist/php-7.4.33/Zend/zend_operators.c | head -5
grep -n "fast_add_function\|fast_long_add" /persist/php-7.4.33/Zend/zend_operators.h | head -10
grep -n "ZEND_ADD_SPEC_CV_CV_HANDLER\|ZEND_VM_HANDLER(2" /persist/php-7.4.33/Zend/zend_vm_execute.h | head -5

echo "[3/12] ruby anchor build (optimizer off, no coverage)"
rm -rf /persist/ruby_anchor
cp -a /persist/ruby-3.3.0 /persist/ruby_anchor
cd /persist/ruby_anchor
./configure CFLAGS="-O0 -g -fwrapv" > /persist/ruby_anchor_configure.log 2>&1
echo "ruby anchor configure exit=$?"
make -j6 ruby > /persist/ruby_anchor_make.log 2>&1
echo "ruby anchor make exit=$? [4/12]"
ls -la /persist/ruby_anchor/ruby

echo "[5/12] ruby ship build (default optimized, no coverage)"
rm -rf /persist/ruby_ship
cp -a /persist/ruby-3.3.0 /persist/ruby_ship
cd /persist/ruby_ship
./configure > /persist/ruby_ship_configure.log 2>&1
echo "ruby ship configure exit=$?"
make -j6 ruby > /persist/ruby_ship_make.log 2>&1
echo "ruby ship make exit=$? [6/12]"
ls -la /persist/ruby_ship/ruby

echo "[7/12] php anchor build (optimizer off, no coverage)"
rm -rf /persist/php_anchor
cp -a /persist/php-7.4.33 /persist/php_anchor
cd /persist/php_anchor
./configure CFLAGS="-O0 -g -fwrapv" > /persist/php_anchor_configure.log 2>&1
echo "php anchor configure exit=$?"
make -j6 > /persist/php_anchor_make.log 2>&1
echo "php anchor make exit=$? [8/12]"
ls -la /persist/php_anchor/sapi/cli/php

echo "[9/12] php ship build (default optimized, no coverage)"
rm -rf /persist/php_ship
cp -a /persist/php-7.4.33 /persist/php_ship
cd /persist/php_ship
./configure > /persist/php_ship_configure.log 2>&1
echo "php ship configure exit=$?"
make -j6 > /persist/php_ship_make.log 2>&1
echo "php ship make exit=$? [10/12]"
ls -la /persist/php_ship/sapi/cli/php

echo "[11/12] gcov-symbol check on all four binaries"
for b in /persist/ruby_anchor/ruby /persist/ruby_ship/ruby /persist/php_anchor/sapi/cli/php /persist/php_ship/sapi/cli/php; do
  echo "=== $b ==="
  nm "$b" 2>&1 | grep -c __gcov || true
done

echo "[12/12] symbol table dumps for candidate handler functions"
mkdir -p /out
for b in /persist/ruby_anchor/ruby /persist/ruby_ship/ruby; do
  echo "=== nm $b (plus/add candidates) ===" >> /out/ruby_nm.txt
  nm -C --defined-only "$b" 2>&1 | grep -iE "plus|vm_opt|fix_plus|big_plus" >> /out/ruby_nm.txt
done
for b in /persist/php_anchor/sapi/cli/php /persist/php_ship/sapi/cli/php; do
  echo "=== nm $b (add candidates) ===" >> /out/php_nm.txt
  nm -C --defined-only "$b" 2>&1 | grep -iE "add_function|add_long|zend_add|zendi_.*add|fast_add" >> /out/php_nm.txt
done
cp /out/ruby_nm.txt /out/php_nm.txt /out/ 2>/dev/null || true
mkdir -p /out/handlers
cp /persist/ruby_anchor/ruby /out/handlers/ruby_anchor_bin 2>&1 || echo "ruby anchor bin missing"
cp /persist/ruby_ship/ruby /out/handlers/ruby_ship_bin 2>&1 || echo "ruby ship bin missing"
cp /persist/php_anchor/sapi/cli/php /out/handlers/php_anchor_bin 2>&1 || echo "php anchor bin missing"
cp /persist/php_ship/sapi/cli/php /out/handlers/php_ship_bin 2>&1 || echo "php ship bin missing"
echo "DONE"
