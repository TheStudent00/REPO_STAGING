#!/bin/bash
set -x
echo "=== probe /persist state ==="
ls -la /persist/ 2>&1
echo "--- ruby ---"
ls -la /persist/ruby 2>&1 | head -5
echo "--- php ---"
ls -la /persist/php 2>&1 | head -5
echo "--- cpython anchor/ship dirs (for reference on structure) ---"
ls -la /persist/cpython_anchor /persist/cpython_ship 2>&1 | head -10
echo "--- network check ---"
curl -sI https://cache.ruby-lang.org/pub/ruby/3.3/ruby-3.3.0.tar.gz 2>&1 | head -5
curl -sI https://www.php.net/distributions/php-7.4.33.tar.gz 2>&1 | head -5
echo "--- gcc/objdump/nm ---"
which gcc objdump nm gcov
