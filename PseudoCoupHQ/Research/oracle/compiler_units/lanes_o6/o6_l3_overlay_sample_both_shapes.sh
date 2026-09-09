#!/usr/bin/env bash
# task o6 lane 3 (resume): build the oracle (12 GB bound, -shape, streamed
# sites, gzip out) and SAMPLE it WITH the overlay for the one generated
# file the checked-in tree lacks (internal/buildcfg/zbootstrap.go, read
# from the image's GOROOT copy) over ONE compiler package,
# cmd/compile/internal/abi (1 file, whose imports pull base/ir/types/obj
# and so the whole closure) -- in BOTH shapes, so each shape's peak RSS
# and wall clock are on record before the full passes. Output to /work.
set -uo pipefail
export GOTOOLCHAIN=local GOPROXY=off GOFLAGS=-mod=mod GO111MODULE=on
export GOCACHE=/work/o6/gocache GOPATH=/work/o6/gopath HOME=/work/o6/home
mkdir -p /work/o6/mod /work/o6/gocache /work/o6/gopath /work/o6/home /work/o6/scratch
OVERLAY=/sources/golang_src/src/internal/buildcfg/zbootstrap.go=/usr/lib/go-1.26/src/internal/buildcfg/zbootstrap.go
echo "[1/5] the other two generated files the tree lacks in cmd/compile's closure are empty package clauses (not overlaid):"
cat /usr/lib/go-1.26/src/cmd/internal/objabi/zbootstrap.go; echo; cat /usr/lib/go-1.26/src/internal/runtime/sys/zversion.go; echo
echo "[2/5] build"
gofmt -l /projects/PseudoCoupHQ/Research/oracle/compiler_units/go_types_oracle.go && echo "gofmt: listed files above need formatting (none = clean)"
cp /projects/PseudoCoupHQ/Research/oracle/compiler_units/go_types_oracle.go /work/o6/mod/main.go
cd /work/o6/mod
printf 'module o6\n\ngo 1.26\n' > go.mod
go build -o /work/o6/oracle . ; echo "build exit: $?"
echo "[3/5] sample, shape=tree, -only internal/abi, GOROOT = source tree, overlay on"
GO111MODULE=off /work/o6/oracle -shape tree -only internal/abi -overlay "$OVERLAY" -scratch /work/o6/scratch -out /work/o6/sample_abi_tree.json.gz ; echo "oracle exit: $?"
echo "[4/5] sample, shape=package, same package"
GO111MODULE=off /work/o6/oracle -shape package -only internal/abi -overlay "$OVERLAY" -scratch /work/o6/scratch -out /work/o6/sample_abi_package.json.gz ; echo "oracle exit: $?"
echo "[5/5] both samples: meta, package record, first 3 sites, and whether the two shapes typed the same sites"
python3 - <<'PY'
import gzip, json
docs = {}
for shape in ("tree", "package"):
    d = json.load(gzip.open(f"/work/o6/sample_abi_{shape}.json.gz", "rt"))
    docs[shape] = d
    m = d["meta"]
    print(f"{shape}: meta: shape={m['shape']} packages={m['packages']} files={m['files']} sites={m['sites']} sites_all_operands_typed={m['sites_all_operands_typed']} elapsed_s={m['elapsed_s']} peak_rss_mb={m['peak_rss_mb']:.1f} overlay={m['overlay']}")
    for p in d["packages"]:
        print(f"{shape}: pkg: {json.dumps(p)}")
    for s in d["sites"][:3]:
        print(f"{shape}: site: {json.dumps(s)}")
key = lambda s: (s["file"], s["line"], s["col"], s["end_line"], s["end_col"], s["kind"], s["operator"], tuple(o["spelling"] for o in s["operands"]), s["result"])
a = sorted(key(s) for s in docs["tree"]["sites"]); b = sorted(key(s) for s in docs["package"]["sites"])
print("same sites (position, kind, label, operand spellings, result) in both shapes:", a == b, "| tree", len(a), "| package", len(b))
PY
echo "[5/5] done"
