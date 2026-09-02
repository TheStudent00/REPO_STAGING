#!/bin/bash
set -x
echo "[1/4] ruby-3.3.0 full listing + count"
find /persist/ruby-3.3.0 -maxdepth 1 | sort
find /persist/ruby-3.3.0 -type f | wc -l
echo "[2/4] the coverage-built /persist/ruby dir (known good, has vm_insnhelper.c per earlier build)"
find /persist/ruby -maxdepth 1 -iname "vm_insnhelper.c" -o -maxdepth 1 -iname "configure" 2>&1
ls /persist/ruby/*.c 2>&1 | head -5
echo "[3/4] php-7.4.33 full listing + count"
find /persist/php-7.4.33 -maxdepth 1 | sort
find /persist/php-7.4.33 -type f | wc -l
echo "[4/4] the coverage-built /persist/php dir"
find /persist/php -maxdepth 1 -iname "configure" 2>&1
ls /persist/php/Zend/*.c 2>&1 | head -5
