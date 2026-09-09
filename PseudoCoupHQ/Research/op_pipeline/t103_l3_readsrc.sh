#!/bin/bash
set -e
echo "[1/2] longobject.c lines 4230-4275, the multiply entry"
sed -n '4230,4275p' /persist/cpython_ship/Objects/longobject.c

echo "[2/2] grep for compact fast-path pattern near long_mul (IS_MEDIUM_VALUE / medium)"
grep -n "IS_MEDIUM_VALUE\|medium_value\|Py_SIZE(a) == 0\|CHECK_SMALL_INT\|_PyLong_IsCompact\|_PyLong_CompactValue" /persist/cpython_ship/Objects/longobject.c | head -30
