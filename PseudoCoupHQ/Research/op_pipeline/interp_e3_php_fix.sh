#!/bin/bash
set -x
echo "[1/6] php anchor: fresh copy, clean, reconfigure without libxml-family ext (core Zend + CLI only)"
rm -rf /persist/php_anchor
cp -a /persist/php /persist/php_anchor
cd /persist/php_anchor
make clean > /persist/php_anchor_clean2.log 2>&1
echo "php anchor clean exit=$?"
./configure CFLAGS="-O0 -g -fwrapv" \
  --disable-libxml --disable-dom --disable-simplexml --disable-xml \
  --disable-xmlreader --disable-xmlwriter --without-pear \
  > /persist/php_anchor_configure2.log 2>&1
echo "php anchor configure exit=$?"
tail -n 30 /persist/php_anchor_configure2.log
make -j6 > /persist/php_anchor_make2.log 2>&1
echo "php anchor make exit=$? [2/6]"
ls -la /persist/php_anchor/sapi/cli/php 2>&1

echo "[3/6] php ship: fresh copy, clean, reconfigure same extension set, default optimization"
rm -rf /persist/php_ship
cp -a /persist/php /persist/php_ship
cd /persist/php_ship
make clean > /persist/php_ship_clean2.log 2>&1
echo "php ship clean exit=$?"
./configure \
  --disable-libxml --disable-dom --disable-simplexml --disable-xml \
  --disable-xmlreader --disable-xmlwriter --without-pear \
  > /persist/php_ship_configure2.log 2>&1
echo "php ship configure exit=$?"
tail -n 30 /persist/php_ship_configure2.log
make -j6 > /persist/php_ship_make2.log 2>&1
echo "php ship make exit=$? [4/6]"
ls -la /persist/php_ship/sapi/cli/php 2>&1

echo "[5/6] gcov-symbol sanity + banner + size diff"
for b in /persist/php_anchor/sapi/cli/php /persist/php_ship/sapi/cli/php; do
  echo "=== $b ==="
  nm "$b" 2>&1 | grep -c __gcov
  "$b" --version 2>&1 | head -1
  stat -c "size=%s" "$b"
done
md5sum /persist/php_anchor/sapi/cli/php /persist/php_ship/sapi/cli/php

echo "[6/6] handler symbol + objdump slice for add_function, plus the two hot generated handlers"
mkdir -p /out/asm
nm -C --defined-only /persist/php_anchor/sapi/cli/php | grep -E " (add_function|ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER|ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER|ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER)$" > /out/php_nm2.txt
nm -C --defined-only /persist/php_ship/sapi/cli/php | grep -E " (add_function|ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER|ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER|ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER)$" >> /out/php_nm2.txt
for sym in add_function ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER; do
  for tag in anchor ship; do
    b="/persist/php_${tag}/sapi/cli/php"
    objdump -d --disassemble="$sym" -M intel "$b" > "/out/asm/php_${tag}_${sym}.txt" 2>&1
  done
done
ls -la /out/asm/php_*
echo DONE
