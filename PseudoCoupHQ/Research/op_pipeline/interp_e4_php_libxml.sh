#!/bin/bash
set -x
echo "[1/2] locate libxml2 pkgconfig / try apt install"
find / -iname "libxml-2.0.pc" 2>/dev/null
pkg-config --exists libxml-2.0 && echo "pkgconfig OK" || echo "pkgconfig MISSING"
apt-get update -qq > /persist/apt_update.log 2>&1; echo "apt-get update exit=$?"
apt-get install -y --no-install-recommends libxml2-dev pkg-config > /persist/apt_install.log 2>&1
echo "apt-get install exit=$?"
tail -n 20 /persist/apt_install.log
pkg-config --exists libxml-2.0 && echo "pkgconfig OK NOW" || echo "still MISSING"

echo "[2/2] retry php anchor+ship configure with default extension set now that libxml2-dev may be present"
rm -rf /persist/php_anchor /persist/php_ship
cp -a /persist/php /persist/php_anchor
cp -a /persist/php /persist/php_ship
cd /persist/php_anchor
make clean > /persist/php_anchor_clean3.log 2>&1
./configure CFLAGS="-O0 -g -fwrapv" > /persist/php_anchor_configure3.log 2>&1
echo "php anchor configure exit=$?"
tail -n 15 /persist/php_anchor_configure3.log
make -j6 > /persist/php_anchor_make3.log 2>&1
echo "php anchor make exit=$?"
ls -la /persist/php_anchor/sapi/cli/php 2>&1

cd /persist/php_ship
make clean > /persist/php_ship_clean3.log 2>&1
./configure > /persist/php_ship_configure3.log 2>&1
echo "php ship configure exit=$?"
tail -n 15 /persist/php_ship_configure3.log
make -j6 > /persist/php_ship_make3.log 2>&1
echo "php ship make exit=$?"
ls -la /persist/php_ship/sapi/cli/php 2>&1

for b in /persist/php_anchor/sapi/cli/php /persist/php_ship/sapi/cli/php; do
  echo "=== $b ==="
  nm "$b" 2>&1 | grep -c __gcov
  stat -c "size=%s" "$b" 2>&1
done
md5sum /persist/php_anchor/sapi/cli/php /persist/php_ship/sapi/cli/php 2>&1

mkdir -p /out/asm
for sym in add_function ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER; do
  for tag in anchor ship; do
    b="/persist/php_${tag}/sapi/cli/php"
    objdump -d --disassemble="$sym" -M intel "$b" > "/out/asm/php_${tag}_${sym}_v2.txt" 2>&1
  done
done
echo DONE
