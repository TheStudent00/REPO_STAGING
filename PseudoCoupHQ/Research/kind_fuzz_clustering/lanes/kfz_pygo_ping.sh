#!/bin/sh
# toolchain ping for the python + go cartesian emitters (log_061).
# Answers two questions and nothing else:
#   1. is the running container bound to AIRLOCK's agent folders?
#   2. is go's toolchain in the image, and what does `go build` cost?
set -u
export HOME=/work
ROOT=/work/kfz_pygo_ping
rm -rf "$ROOT"; mkdir -p "$ROOT"
echo "=== kfz pygo ping ==="
date -u +%Y-%m-%dT%H:%M:%SZ
echo "[progress] ping [1/4] toolchain versions"
python3 --version 2>&1 || echo "python3 MISSING"
ruby -v 2>&1 || echo "ruby MISSING"
rustc --version 2>&1 || echo "rustc MISSING"
go version 2>&1 || echo "go MISSING"
echo "[progress] ping [2/4] go build, 200 trivial probe functions"
export GOTOOLCHAIN=local
export GOPROXY=off
export GOFLAGS=-mod=mod
export GOCACHE="$ROOT/gocache"
export GOPATH="$ROOT/gopath"
mkdir -p "$ROOT/g"
printf 'module chunk\n\ngo 1.26\n' > "$ROOT/g/go.mod"
{
  echo 'package main'
  echo ''
  echo 'import ('
  echo '	"bufio"'
  echo '	"fmt"'
  echo '	"math"'
  echo '	"os"'
  echo '	"reflect"'
  echo '	"sort"'
  echo '	"strconv"'
  echo '	"strings"'
  echo ')'
  echo ''
  echo 'var _W = bufio.NewWriterSize(os.Stdout, 1<<14)'
  echo 'var _ = math.Copysign'
  echo 'var _ = sort.Strings'
  echo 'var _ = strings.Join'
  echo 'var _ = strconv.FormatUint'
  echo 'var _ = reflect.TypeOf'
  echo 'var _ = fmt.Sprint'
  i=0
  while [ "$i" -lt 200 ]; do
    echo "func p$i() { var a int64 = $i; var b int64 = 3; _r := (a) + (b); fmt.Fprintf(_W, \"p$i|%v\\n\", _r) }"
    i=$((i + 1))
  done
  echo 'func main() {'
  i=0
  while [ "$i" -lt 200 ]; do
    echo "	p$i()"
    i=$((i + 1))
  done
  echo '	_W.Flush()'
  echo '}'
} > "$ROOT/g/chunk.go"
S=$(date +%s.%N)
( cd "$ROOT/g" && go build -o "$ROOT/g/bin" chunk.go ) 2>&1 | head -20
E=$(date +%s.%N)
echo "go build 200 probes: $(echo "$E - $S" | bc) s"
echo "[progress] ping [3/4] run it"
"$ROOT/g/bin" | tail -2
echo "[progress] ping [4/4] negative zero and constant rules in go"
cat > "$ROOT/g/nz.go" <<'GO_EOF'
package main

import (
	"fmt"
	"math"
)

func main() {
	var a float64 = -0.0
	var b float64 = math.Copysign(0, -1)
	var c float64 = 5e-324
	var d float32 = 9007199254740992
	fmt.Printf("literal -0.0 signbit=%v\n", math.Signbit(a))
	fmt.Printf("Copysign(0,-1) signbit=%v\n", math.Signbit(b))
	fmt.Printf("5e-324 bits=%016x\n", math.Float64bits(c))
	fmt.Printf("f32 2^53 bits=%08x\n", math.Float32bits(d))
}
GO_EOF
( cd "$ROOT/g" && go run nz.go ) 2>&1 | head -10
rm -rf "$ROOT"
date -u +%Y-%m-%dT%H:%M:%SZ
echo "=== kfz pygo ping done ==="
