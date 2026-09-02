#!/bin/bash
set -x
echo "[1/14] grep ruby handler candidates (source at /persist/ruby, the full tree from the coverage build)"
grep -n "vm_opt_plus" /persist/ruby/vm_insnhelper.c | head -10
grep -n "rb_fix_plus\|fix_plus\|rb_int_plus" /persist/ruby/numeric.c | head -10
grep -n "rb_big_plus\|bignum.*plus" /persist/ruby/bignum.c | grep -i plus | head -10

echo "[2/14] grep php handler candidates (source at /persist/php)"
grep -n "^add_function\|ZEND_API.*add_function" /persist/php/Zend/zend_operators.c | head -5
grep -n "fast_add_function\|fast_long_add" /persist/php/Zend/zend_operators.h | head -10
grep -n "ZEND_ADD_SPEC" /persist/php/Zend/zend_vm_execute.h | head -10

echo "[3/14] ruby anchor: copy full coverage-built tree, clean, reconfigure without coverage"
rm -rf /persist/ruby_anchor
cp -a /persist/ruby /persist/ruby_anchor
cd /persist/ruby_anchor
make distclean > /persist/ruby_anchor_distclean.log 2>&1
echo "ruby anchor distclean exit=$?"
./configure CFLAGS="-O0 -g -fwrapv" > /persist/ruby_anchor_configure.log 2>&1
echo "ruby anchor configure exit=$?"
make -j6 ruby > /persist/ruby_anchor_make.log 2>&1
echo "ruby anchor make exit=$? [4/14]"
ls -la /persist/ruby_anchor/ruby 2>&1

echo "[5/14] ruby ship: copy full tree, clean, reconfigure default optimized"
rm -rf /persist/ruby_ship
cp -a /persist/ruby /persist/ruby_ship
cd /persist/ruby_ship
make distclean > /persist/ruby_ship_distclean.log 2>&1
echo "ruby ship distclean exit=$?"
./configure > /persist/ruby_ship_configure.log 2>&1
echo "ruby ship configure exit=$?"
make -j6 ruby > /persist/ruby_ship_make.log 2>&1
echo "ruby ship make exit=$? [6/14]"
ls -la /persist/ruby_ship/ruby 2>&1

echo "[7/14] php anchor: copy full tree, clean, reconfigure without coverage"
rm -rf /persist/php_anchor
cp -a /persist/php /persist/php_anchor
cd /persist/php_anchor
make clean > /persist/php_anchor_clean.log 2>&1
echo "php anchor clean exit=$?"
./configure CFLAGS="-O0 -g -fwrapv" > /persist/php_anchor_configure.log 2>&1
echo "php anchor configure exit=$?"
make -j6 > /persist/php_anchor_make.log 2>&1
echo "php anchor make exit=$? [8/14]"
ls -la /persist/php_anchor/sapi/cli/php 2>&1

echo "[9/14] php ship: copy full tree, clean, reconfigure default optimized"
rm -rf /persist/php_ship
cp -a /persist/php /persist/php_ship
cd /persist/php_ship
make clean > /persist/php_ship_clean.log 2>&1
echo "php ship clean exit=$?"
./configure > /persist/php_ship_configure.log 2>&1
echo "php ship configure exit=$?"
make -j6 > /persist/php_ship_make.log 2>&1
echo "php ship make exit=$? [10/14]"
ls -la /persist/php_ship/sapi/cli/php 2>&1

echo "[11/14] gcov-symbol sanity check (must be zero on all four)"
for b in /persist/ruby_anchor/ruby /persist/ruby_ship/ruby /persist/php_anchor/sapi/cli/php /persist/php_ship/sapi/cli/php; do
  echo "=== $b ==="
  nm "$b" 2>&1 | grep -c __gcov
done

echo "[12/14] handler symbol tables"
mkdir -p /out
: > /out/ruby_nm.txt
: > /out/php_nm.txt
for b in /persist/ruby_anchor/ruby /persist/ruby_ship/ruby; do
  echo "=== nm $b ===" >> /out/ruby_nm.txt
  nm -C --defined-only "$b" 2>&1 | grep -iE "plus|opt_plus|fix_plus|big_plus" >> /out/ruby_nm.txt
done
for b in /persist/php_anchor/sapi/cli/php /persist/php_ship/sapi/cli/php; do
  echo "=== nm $b ===" >> /out/php_nm.txt
  nm -C --defined-only "$b" 2>&1 | grep -iE "add_function|fast_add|zendi_.*add|zend_add" >> /out/php_nm.txt
done

echo "[13/14] objdump handler slices (attempted for likely symbols)"
mkdir -p /out/asm
for sym in vm_opt_plus rb_fix_plus rb_int_plus rb_big_plus; do
  for tag in anchor ship; do
    b="/persist/ruby_${tag}/ruby"
    objdump -d --disassemble="$sym" -M intel "$b" > "/out/asm/ruby_${tag}_${sym}.txt" 2>&1
  done
done
for sym in add_function; do
  for tag in anchor ship; do
    b="/persist/php_${tag}/sapi/cli/php"
    objdump -d --disassemble="$sym" -M intel "$b" > "/out/asm/php_${tag}_${sym}.txt" 2>&1
  done
done

echo "[14/14] done, listing /out"
ls -la /out/asm/
echo DONE
