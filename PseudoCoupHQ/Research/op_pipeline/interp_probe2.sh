#!/bin/bash
set -x
echo "[1/2] ruby source tree"
ls -la /persist/ruby-3.3.0/ | head -30
find /persist/ruby-3.3.0 -maxdepth 2 -iname "configure" 2>&1
find /persist/ruby-3.3.0 -maxdepth 2 -iname "vm_insnhelper.c" 2>&1
echo "[2/2] php source tree"
ls -la /persist/php-7.4.33/ | head -30
find /persist/php-7.4.33 -maxdepth 2 -iname "configure" 2>&1
find /persist/php-7.4.33 -maxdepth 3 -iname "zend_operators.c" 2>&1
