#!/usr/bin/env bash
# task o6 lane 1: build go_types_oracle.go inside the instance and run it
# over ONE compiler package (cmd/compile/internal/abi, 1 file) with GOROOT
# at the source tree, so the memory sample (peak RSS) is on record before
# the full run. Output goes to /work (scratch), not the artifact folder.
set -uo pipefail
export GOTOOLCHAIN=local GOPROXY=off GOFLAGS=-mod=mod GO111MODULE=on
export GOCACHE=/work/o6/gocache GOPATH=/work/o6/gopath HOME=/work/o6/home
mkdir -p /work/o6/mod /work/o6/gocache /work/o6/gopath /work/o6/home
echo "[1/4] toolchain and source-tree identity"
go version
go env GOROOT
head -12 /sources/golang_src/src/internal/goversion/goversion.go | grep -n "Version"
grep -n "^go " /sources/golang_src/src/go.mod
echo "[2/4] build"
cp PseudoCoupHQ/Research/oracle/compiler_units/go_types_oracle.go /work/o6/mod/main.go
cd /work/o6/mod
printf 'module o6\n\ngo 1.26\n' > go.mod
gofmt -l main.go && echo "gofmt: listed files above need formatting (none = clean)"
go build -o /work/o6/oracle . ; echo "build exit: $?"
echo "[3/4] sample: -only internal/abi, GOROOT = source tree"
GO111MODULE=off /work/o6/oracle -only internal/abi -out /work/o6/sample_abi.json ; echo "oracle exit: $?"
echo "[4/4] sample output head"
head -c 1500 /work/o6/sample_abi.json; echo
python3 -c "
import json; d=json.load(open('/work/o6/sample_abi.json'))
print('meta:', json.dumps(d['meta']))
for p in d['packages']: print('pkg:', json.dumps(p))
print('first 3 sites:')
for s in d['sites'][:3]: print(json.dumps(s))
"
echo "[4/4] done"
