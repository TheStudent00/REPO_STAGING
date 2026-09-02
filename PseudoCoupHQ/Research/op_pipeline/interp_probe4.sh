#!/bin/bash
set -x
echo "[1/2] php anchor configure log tail"
tail -n 60 /persist/php_anchor_configure.log
echo "[2/2] check for stale config.status / Makefile after make clean"
ls -la /persist/php_anchor/config.status /persist/php_anchor/Makefile 2>&1
grep -m2 "extra_include_paths\|CFLAGS" /persist/php_anchor/main/build-defs.h 2>&1
grep -c "distclean:" /persist/php/Makefile.objects /persist/php/Makefile.global 2>&1
