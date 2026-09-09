#!/bin/bash
set -e
echo "[1/1] objdump long_mul, tail (0x1396f0 to end)"
objdump -d -w --start-address=0x1396f0 --stop-address=0x139782 /persist/cpython_ship/python
