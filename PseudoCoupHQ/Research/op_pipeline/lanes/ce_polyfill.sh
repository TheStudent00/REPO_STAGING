#!/bin/sh
# the owner's polyfill question, measured on the cheap case:
# go's `&^` (and-not) is a singleton dom_op — no other language has
# the operator. Polyfill it in c and rust from their basic operators
# and compare the SHIP arch-units against go's native one.
set -u
export HOME=/work
ROOT=/work/polyfill; rm -rf "$ROOT"; mkdir -p "$ROOT"; cd "$ROOT"
OUT=/out/ce_polyfill.txt; : > "$OUT"
say(){ echo "$@" >> "$OUT"; }
dis(){ objdump -d --disassemble="$2" "$1" 2>/dev/null \
  | grep -E "^\s+[0-9a-f]+:" \
  | sed 's/^[[:space:]]*[0-9a-f]*:[[:space:]]*//'; }

say "=== go native &^ (and-not) on i64 ==="
mkdir -p gm && cd gm
cat > m.go <<'EOF'
package main

//go:noinline
func andnot(a, b int64) int64 { return a &^ b }

func main() { println(andnot(7, 3)) }
EOF
printf 'module m\n\ngo 1.26\n' > go.mod
GOTOOLCHAIN=local GOPROXY=off GOFLAGS=-mod=mod \
GOCACHE="$ROOT/gc" GOPATH="$ROOT/gp" go build -o gobin . 2>>"$OUT"
dis gobin main.andnot >> "$OUT"
cd "$ROOT"

say ""
say "=== c polyfill: a & ~b ==="
cat > p.c <<'EOF'
#include <stdint.h>
int64_t andnot(int64_t a, int64_t b) { return a & ~b; }
EOF
/usr/bin/clang -O1 -c -o p.o p.c 2>>"$OUT"
dis p.o andnot >> "$OUT"

say ""
say "=== rust polyfill: a & !b ==="
cat > p.rs <<'EOF'
#[no_mangle]
pub fn andnot(a: i64, b: i64) -> i64 { a & !b }
EOF
rustc --crate-type=lib --emit=obj -C opt-level=1 -o pr.o p.rs 2>>"$OUT"
dis pr.o andnot >> "$OUT"

say ""
say "=== the wrapped shape (polyfill as a helper fn, then inlined use) ==="
cat > w.c <<'EOF'
#include <stdint.h>
static inline int64_t go_andnot(int64_t a, int64_t b) { return a & ~b; }
int64_t use(int64_t a, int64_t b) { return go_andnot(a, b); }
EOF
/usr/bin/clang -O1 -c -o w.o w.c 2>>"$OUT"
dis w.o use >> "$OUT"
say ""; say "done."
