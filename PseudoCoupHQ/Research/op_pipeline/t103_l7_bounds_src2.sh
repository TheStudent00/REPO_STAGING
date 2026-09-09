#!/bin/bash
echo "[1/2] pycore_long.h lines 178-260"
sed -n '178,260p' /persist/cpython_ship/Include/internal/pycore_long.h
echo "[2/2] PyLong_SHIFT / BASE / MASK / NON_SIZE_BITS"
grep -rn "define PyLong_SHIFT\|define PyLong_BASE\|define PyLong_MASK\|define _PyLong_NON_SIZE_BITS\|define NON_SIZE_BITS" /persist/cpython_ship/Include/*.h /persist/cpython_ship/Include/**/*.h 2>/dev/null
