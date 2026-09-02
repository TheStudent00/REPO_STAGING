#!/bin/bash
# Task 27 -- php: (a) dump the handler slices from the builds that exist,
# recording their gcov contamination honestly; (b) ONE time-boxed attempt
# at a clean, uninstrumented anchor/ship pair from a fresh tarball
# extraction with every bundled extension disabled, so php's configure
# never reaches its libxml-2.0 probe (the wall recorded in log_095).
set -x
mkdir -p /out/t27

echo "[1/6] contamination record for the builds that exist now"
for tag in anchor ship; do
  b="/persist/php_${tag}/sapi/cli/php"
  echo "=== $b"
  ls -la "$b"
  md5sum "$b"
  nm "$b" 2>/dev/null | grep -c gcov
done
diff <(objdump -d --disassemble=add_function /persist/php_anchor/sapi/cli/php) \
     <(objdump -d --disassemble=add_function /persist/php_ship/sapi/cli/php) \
     > /out/t27/php_existing_anchor_ship_diff.txt 2>&1
echo "existing anchor-vs-ship add_function diff lines=$(wc -l < /out/t27/php_existing_anchor_ship_diff.txt)"

echo "[2/6] raw objdump text from the existing (instrumented) build"
for sym in add_function ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER; do
  for tag in anchor ship; do
    b="/persist/php_${tag}/sapi/cli/php"
    objdump -d --disassemble="$sym" "$b" > "/out/t27/phpcov_${tag}_${sym}.txt" 2>&1
    echo "$sym $tag lines=$(wc -l < /out/t27/phpcov_${tag}_${sym}.txt)"
  done
  nm "/persist/php_anchor/sapi/cli/php" 2>/dev/null | grep " $sym$"
done

echo "[3/6] fresh extraction of the pinned tarball, twice"
rm -rf /persist/php_c_anchor /persist/php_c_ship /persist/php_c_src
mkdir -p /persist/php_c_src
tar xzf /persist/php-7.4.33.tar.gz -C /persist/php_c_src
ls /persist/php_c_src
SRC=$(ls -d /persist/php_c_src/php-7.4.33)
echo "src=$SRC files=$(find $SRC -type f | wc -l)"
cp -a "$SRC" /persist/php_c_anchor
cp -a "$SRC" /persist/php_c_ship

echo "[4/6] anchor configure+make, every extension off"
cd /persist/php_c_anchor
./configure --disable-all --disable-libxml --disable-dom --disable-simplexml \
  --disable-xml --disable-xmlreader --disable-xmlwriter --without-pear \
  --without-sqlite3 --without-pdo-sqlite --disable-phar --disable-cgi \
  CFLAGS="-O0 -g -fwrapv" > /persist/php_c_anchor_configure.log 2>&1
echo "php clean anchor configure exit=$?"
tail -n 12 /persist/php_c_anchor_configure.log
make -j6 > /persist/php_c_anchor_make.log 2>&1
echo "php clean anchor make exit=$?"
tail -n 5 /persist/php_c_anchor_make.log
ls -la /persist/php_c_anchor/sapi/cli/php 2>&1

echo "[5/6] ship configure+make, same extension set, optimizer on"
cd /persist/php_c_ship
./configure --disable-all --disable-libxml --disable-dom --disable-simplexml \
  --disable-xml --disable-xmlreader --disable-xmlwriter --without-pear \
  --without-sqlite3 --without-pdo-sqlite --disable-phar --disable-cgi \
  CFLAGS="-O2 -g" > /persist/php_c_ship_configure.log 2>&1
echo "php clean ship configure exit=$?"
tail -n 12 /persist/php_c_ship_configure.log
make -j6 > /persist/php_c_ship_make.log 2>&1
echo "php clean ship make exit=$?"
tail -n 5 /persist/php_c_ship_make.log
ls -la /persist/php_c_ship/sapi/cli/php 2>&1

echo "[6/6] if both built: contamination check, version pin, raw dumps"
for tag in anchor ship; do
  b="/persist/php_c_${tag}/sapi/cli/php"
  if [ -x "$b" ]; then
    echo "=== $b"
    md5sum "$b"
    nm "$b" 2>/dev/null | grep -c gcov
    "$b" -v 2>&1 | head -2
    for sym in add_function ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER; do
      objdump -d --disassemble="$sym" "$b" > "/out/t27/phpclean_${tag}_${sym}.txt" 2>&1
      echo "$sym $tag lines=$(wc -l < /out/t27/phpclean_${tag}_${sym}.txt)"
    done
    nm "$b" 2>/dev/null | grep -E " (add_function|ZEND_ADD_[A-Z_]*HANDLER)$" > "/out/t27/phpclean_${tag}_nm.txt"
    wc -l "/out/t27/phpclean_${tag}_nm.txt"
  else
    echo "NO CLEAN BINARY for $tag -- recorded as a refusal, nothing passed off"
  fi
done
cp /persist/php_c_anchor_configure.log /persist/php_c_ship_configure.log /out/t27/ 2>&1
echo DONE
