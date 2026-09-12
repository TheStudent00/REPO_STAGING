#!/bin/bash
# rv4_l1_the_sample_of_five_pairs.sh -- task rv4, lane 1: the sample the law
# asks for BEFORE the round -- the three optimization-off compile routes
# probed one by one, the population built and put through the spelling
# guard, and FIVE (cell, target) pairs run one after another with the
# seconds each took and the peak resident the sample reached.
#
#   [1/6] the three optimization-off routes, each probed on its own
#   [2/6] the population: every cell whose term the lifter states, on each
#         target with no proved certificate, decided on machine form
#   [3/6] the spelling guard over the population
#   [4/6] the sample: five pairs spread over the population
#   [5/6] the sample's rows, as they were written
#   [6/6] peak resident
#
# MEMORY: bound 6 GB resident per worker, named abort ABORT_MEMORY_RV4.
#
# Node: hq.research.arch_unit_oracle.architectures.riscv64
# Brief: Research/briefs/task_rv4_brief.md
set -u

P=PseudoCoupHQ
RV=$P/Research/oracle/riscv
OP=$P/Research/op_pipeline
export HOME=/work
export GOCACHE=/work/rv4gocache GOPATH=/work/rv4gopath
mkdir -p "$GOCACHE" "$GOPATH" /work/rv4work /work/rv4probe
total=6

i=1
echo "[$i/$total] the three optimization-off routes, each probed on its own"
cat > /work/rv4probe/probe.c <<'EOF'
#include <stdint.h>
uint64_t emu_probe(uint64_t a, uint64_t b) { return a * b; }
EOF
clang -std=c17 -O0 --target=riscv64-linux-gnu --gcc-toolchain=/usr \
  -c /work/rv4probe/probe.c -o /work/rv4probe/probe.o
echo "  clang c riscv64 -O0 rc=$?"
cat > /work/rv4probe/probe.rs <<'EOF'
#[no_mangle]
pub extern "C" fn emu_probe(a: u64, b: u64) -> u64 { a.wrapping_mul(b) }
EOF
rustc --crate-type=lib --emit=obj -C opt-level=0 -C debug-assertions=off \
  --target=riscv64gc-unknown-linux-gnu -o /work/rv4probe/probe_rs.o \
  /work/rv4probe/probe.rs
echo "  rustc riscv64 opt-level=0 rc=$?"
mkdir -p /work/rv4probe/go
cat > /work/rv4probe/go/go.mod <<'EOF'
module opprobe

go 1.26
EOF
cat > /work/rv4probe/go/main.go <<'EOF'
package main

func emu_probe(a uint64, b uint64) uint64 { return a * b }

func main() { println(emu_probe(3, 4)) }
EOF
( cd /work/rv4probe/go && GOARCH=riscv64 GOOS=linux GOTOOLCHAIN=local \
    GOPROXY=off GOFLAGS=-mod=mod go build -gcflags 'all=-N -l' -o bin_rv . )
echo "  go build riscv64 -gcflags='all=-N -l' rc=$?"
echo "  the carve, on the c probe:"
llvm-objdump -dr -M no-aliases --mattr=+m,+a,+f,+d,+c \
  --disassemble-symbols=emu_probe /work/rv4probe/probe.o | tail -8
echo "  clang: $(clang --version | head -1)"
echo "  rustc: $(rustc --version)"
echo "  go:    $(go version)"
echo "  llvm-objdump: $(llvm-objdump --version | head -2 | tail -1)"

i=2
echo ""
echo "[$i/$total] the population"
timeout 900 python3 "$RV/rv4_off.py" population "$P" \
  "$RV/rv4_population.json"
echo "  exit: $?"

i=3
echo ""
echo "[$i/$total] the spelling guard over the population"
python3 "$OP/check_no_spelling_keys.py" "$RV/rv4_population.json"
echo "  guard rc=$?"

i=4
echo ""
echo "[$i/$total] the sample: five pairs spread over the population"
timeout 900 python3 "$RV/rv4_off.py" sample "$P" \
  "$RV/rv4_population.json" 5 "$RV/rv4_sample" "$RV/src_rv4_sample" \
  /work/rv4work
echo "  exit: $?"

i=5
echo ""
echo "[$i/$total] the sample's rows, as they were written"
python3 -c "
import json, sys
rows = [json.loads(l) for l in open('$RV/rv4_sample.jsonl')]
for row in rows:
    cell = row['cell']
    print('  %s %s %s %s on %s -> %s in %.2f s, %s instructions' % (
        cell['mnem'], cell['shape'], cell['key_width'], row['place'],
        row['target'], row['outcome'], row['seconds'],
        row.get('instructions')))
    verdict = row.get('verdict') or {}
    if verdict.get('reason'):
        print('      reason: %s' % verdict['reason'][:200])
    calls = row.get('gate_calls') or []
    if calls:
        print('      the gate: text_taken=%s, %s nodes against %s, %.3f s'
              % (calls[0]['text_taken'], calls[0]['left_nodes'],
                 calls[0]['right_nodes'], calls[0]['seconds']))
"
echo "  exit: $?"

i=6
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
