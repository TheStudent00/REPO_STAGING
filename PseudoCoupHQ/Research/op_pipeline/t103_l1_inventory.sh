#!/bin/bash
set -e
echo "[1/6] python --version and sysconfig JIT vars"
/persist/cpython_ship/python --version
/persist/cpython_ship/python -c "import sysconfig; print('PY_CORE_CFLAGS=', sysconfig.get_config_var('PY_CORE_CFLAGS'))"
/persist/cpython_ship/python -c "import sysconfig; print('CONFIG_ARGS=', sysconfig.get_config_var('CONFIG_ARGS'))"
/persist/cpython_ship/python -c "import sys; print('_Py_JIT' , hasattr(sys, '_jit') if hasattr(sys,'_jit') else 'no sys._jit attr')"

echo "[2/6] search for _Py_JIT / jit_stencils in the ship binary and source"
strings /persist/cpython_ship/python | grep -c "_Py_JIT" || true
strings /persist/cpython_ship/python | grep -i "jit" | head -20 || true

echo "[3/6] find any jit_stencils.h anywhere reachable"
find /persist -iname "jit_stencils.h" 2>/dev/null | head
find /sources -iname "jit_stencils.h" 2>/dev/null | head

echo "[4/6] locate the cpython source tree if mounted"
find /sources -maxdepth 3 -iname "*cpython*" -o -iname "*Python-3.14*" 2>/dev/null | head -20
find / -maxdepth 4 -iname "longobject.c" 2>/dev/null | head -10

echo "[5/6] symbol table: candidate multiply handler names"
readelf -sW /persist/cpython_ship/python | grep -iE "\blong_mul\b|_PyLong_Multiply|long_mul_fastpath|x_mul|k_mul" || true

echo "[6/6] anchor build present too?"
ls -la /persist/cpython_anchor/ 2>&1 | head -5
/persist/cpython_anchor/python --version 2>&1 || true
