#!/bin/bash
set -e
echo "[1/4] sys._jit introspection, literal"
/persist/cpython_ship/python -c "
import sys
print('hasattr sys._jit:', hasattr(sys, '_jit'))
if hasattr(sys, '_jit'):
    print('sys._jit.is_available():', sys._jit.is_available())
    print('sys._jit.is_enabled():', sys._jit.is_enabled())
    print('sys._jit.is_active():', sys._jit.is_active())
"
echo "[2/4] configure args / config.h for the JIT macro, literal grep"
grep -n "_Py_JIT\|JIT_STENCILS\|experimental-jit" /persist/cpython_ship/pyconfig.h 2>/dev/null || echo "no pyconfig.h at that path"
find /persist/cpython_ship -maxdepth 2 -iname "pyconfig.h" 2>/dev/null
find /persist/cpython_ship -iname "jit_stencils.h" 2>/dev/null
find /persist/cpython_ship -maxdepth 1 -iname "config.log" 2>/dev/null

echo "[3/4] longobject.c -- the multiply handler and its callers, line numbers"
grep -n "^long_mul\|^_PyLong_Multiply\|^static PyObject \*\s*$\|nb_multiply\|long_mul(" /persist/cpython_ship/Objects/longobject.c | head -40

echo "[4/4] the two candidate function bodies, with line numbers"
awk '/^_?long_mul\(/{print NR": "$0} /^_PyLong_Multiply\(/{print NR": "$0}' /persist/cpython_ship/Objects/longobject.c
