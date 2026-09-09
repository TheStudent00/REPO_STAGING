#!/bin/bash
set -e
echo "[1/3] _PyLong_BothAreCompact / _PyLong_IsCompact / medium_value / PyLong_SHIFT"
grep -rn "_PyLong_BothAreCompact\|_PyLong_IsCompact\b\|define medium_value\|PyLong_SHIFT\b\|_PyLong_NON_SIZE_BITS\|_PyLong_CompactValue" /persist/cpython_ship/Include/internal/pycore_long.h 2>/dev/null | head -40

echo "[2/3] the compact predicate's own body"
sed -n '1,50p' /persist/cpython_ship/Include/internal/pycore_long.h | grep -n "static inline\|BothAreCompact\|IsCompact" 
grep -n "static inline.*_PyLong_IsCompact\|static inline.*_PyLong_BothAreCompact\|static inline.*_PyLong_CompactValue" -A 6 /persist/cpython_ship/Include/internal/pycore_long.h

echo "[3/3] PyLong_SHIFT and digit width"
grep -rn "define PyLong_SHIFT\|define PyLong_BASE\|define PyLong_MASK" /persist/cpython_ship/Include/internal/pycore_long.h /persist/cpython_ship/Include/cpython/longintrepr.h 2>/dev/null
