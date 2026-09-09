#!/bin/bash
set -e
echo "[1/2] objdump the whole long_mul body, symbol-relative"
objdump -d -w --start-address=0x1394f0 --stop-address=0x139756 /persist/cpython_ship/python | sed -n '1,140p'
echo "[2/2] is _PyLong_FromSTwoDigits its own symbol"
readelf -sW /persist/cpython_ship/python | grep -i "FromSTwoDigits\|FromMedium"
