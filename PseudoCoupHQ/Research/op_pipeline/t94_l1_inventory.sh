#!/bin/bash
set -x
echo "[1/8] persist inventory"
ls -la /persist/ 2>&1 | head -60
echo "[2/8] cpython ship/anchor binaries"
ls -la /persist/cpython_ship/python /persist/cpython_anchor/python 2>&1
echo "[3/8] ruby ship/anchor"
ls -la /persist/ruby_ship/ruby /persist/ruby_anchor/ruby 2>&1
echo "[4/8] php ship/anchor"
ls -la /persist/php_ship/sapi/cli/php /persist/php_anchor/sapi/cli/php 2>&1
echo "[5/8] toolchain"
which objdump readelf nm python3 2>&1
objdump --version 2>&1 | head -2
python3 -c "import z3,pyvex,archinfo,capstone,elftools;print('z3',z3.get_version_string());print('pyvex ok');print('capstone',capstone.__version__)" 2>&1
echo "[6/8] symbol table for long_add in cpython ship"
nm -C /persist/cpython_ship/python 2>&1 | grep -w long_add | head
readelf -sW /persist/cpython_ship/python 2>&1 | grep -w long_add | head
echo "[7/8] ruby symbols"
readelf -sW /persist/ruby_ship/ruby 2>&1 | grep -wE "rb_fix_plus|rb_int_plus|rb_big_plus|vm_opt_plus" | head -20
echo "[8/8] php symbols"
readelf -sW /persist/php_ship/sapi/cli/php 2>&1 | grep -wE "add_function|ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER|ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER|ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER" | head -20
echo done
