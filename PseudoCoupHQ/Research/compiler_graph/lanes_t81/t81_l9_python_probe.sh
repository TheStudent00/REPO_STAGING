#!/usr/bin/env bash
# t81 lane 9 — WHICH interpreter in this image can import tree_sitter.
#
# Lane 6 stopped at `ModuleNotFoundError: No module named 'tree_sitter'`
# from the container's default `python3`, while the round-15 brief
# records the image as carrying tree-sitter 0.25.2. So the module is
# somewhere this PATH does not reach. This lane finds out WHERE rather
# than guessing, and installs nothing.
set -u
say() { echo; echo "======== $* ========"; }

say "the default interpreter"
which -a python3 python 2>&1
python3 --version
python3 -c "import sys; print(sys.executable); print(sys.path)"

say "every python on the filesystem"
ls -1 /usr/bin/python3* /usr/local/bin/python3* /opt/*/bin/python3* \
      /opt/*/*/bin/python3* 2>/dev/null

say "every venv-looking tree"
ls -d /opt/* /srv/* /usr/local/lib/python3* 2>/dev/null | head -20

say "where tree_sitter lives, if it is on disk at all"
find / -maxdepth 8 -name 'tree_sitter' -type d 2>/dev/null | head -10
find / -maxdepth 8 -name 'tree_sitter*' -maxdepth 8 2>/dev/null | head -20

say "the imports this task needs, tried on every interpreter found"
for P in $(ls -1 /usr/bin/python3* /usr/local/bin/python3* /opt/*/bin/python3* \
                 /opt/*/*/bin/python3* 2>/dev/null | sort -u) ; do
  [ -x "$P" ] || continue
  printf '   %-40s ' "$P"
  "$P" - <<'PY' 2>&1 | tr '\n' ' '
try:
    import tree_sitter
    print('tree_sitter', tree_sitter.__version__ if hasattr(tree_sitter, '__version__') else 'ok', end=' ')
except Exception as problem:
    print('tree_sitter MISSING', end=' ')
for name in ('tree_sitter_c', 'tree_sitter_cpp', 'pyvex', 'archinfo',
             'capstone', 'elftools', 'z3'):
    try:
        __import__(name)
        print(name, end=' ')
    except Exception:
        print(name + '-MISSING', end=' ')
PY
  echo
done
echo "DONE t81_l9"
