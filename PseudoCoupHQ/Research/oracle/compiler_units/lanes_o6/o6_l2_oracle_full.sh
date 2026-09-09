#!/usr/bin/env bash
# task o6 lane 2: the full go/types pass over src/cmd/compile/..., GOROOT at
# the source tree, writing the deliverable go_types_sites.json.
set -uo pipefail
export GOTOOLCHAIN=local GOPROXY=off GOFLAGS=-mod=mod GO111MODULE=on
export GOCACHE=/work/o6/gocache GOPATH=/work/o6/gopath HOME=/work/o6/home
mkdir -p /work/o6/mod /work/o6/gocache /work/o6/gopath /work/o6/home
echo "[1/3] build (same source as lane 1)"
cp PseudoCoupHQ/Research/oracle/compiler_units/go_types_oracle.go /work/o6/mod/main.go
cd /work/o6/mod
printf 'module o6\n\ngo 1.26\n' > go.mod
go build -o /work/o6/oracle . ; echo "build exit: $?"
echo "[2/3] full run: root /sources/golang_src/src/cmd/compile, GOROOT /sources/golang_src"
GO111MODULE=off /work/o6/oracle -root /sources/golang_src/src/cmd/compile -goroot /sources/golang_src \
  -out PseudoCoupHQ/Research/oracle/compiler_units/go_types_sites.json ; echo "oracle exit: $?"
echo "[3/3] output size and meta"
ls -l PseudoCoupHQ/Research/oracle/compiler_units/go_types_sites.json
python3 -c "
import json; d=json.load(open('PseudoCoupHQ/Research/oracle/compiler_units/go_types_sites.json'))
print('meta:', json.dumps(d['meta']))
"
echo "[3/3] done"
