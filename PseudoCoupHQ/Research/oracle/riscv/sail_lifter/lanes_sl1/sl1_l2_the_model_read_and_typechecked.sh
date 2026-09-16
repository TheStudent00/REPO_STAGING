#!/bin/bash
# sl1 lane 2 -- the parts of the model the generator must know, LITERAL
# (the project file, the register file access, xlen, the execute result
# type, the extension check), and the cost of one whole-model typecheck.
set -u
total=7
export HOME=/work
M=/sources/sail-riscv
echo "[1/$total] the project file"
cat $M/model/riscv.sail_project 2>&1 | head -150
echo "[2/$total] the register file access (regs.sail), xlen, regidx"
sed -n '140,250p' $M/model/core/regs.sail
grep -rn 'type xlen\|xlen :\|xlen =' $M/model/prelude $M/model/core 2>/dev/null | head -10
grep -rn 'type regidx\|newtype regidx\|struct regidx\|type cregidx\|type fregidx\|type regno' $M/model --include='*.sail' | head
grep -rn 'overload X\|function X\|val X ' $M/model --include='*.sail' | head
echo "[3/$total] the execute function type, the result, the extension check"
grep -rn 'scattered function execute\|val execute\|scattered union instruction\|type ExecutionResult\|union ExecutionResult\|RETIRE_SUCCESS\b' $M/model --include='*.sail' | head -12
grep -rn -B2 -A12 'function extensionEnabled\|function currentlyEnabled' $M/model/core/*.sail $M/model/sys/*.sail 2>/dev/null | head -60
grep -rn 'currentlyEnabled(Ext_M)\|extensionEnabled(Ext_M)' $M/model --include='*.sail' | head -3
echo "[4/$total] two execute clauses, LITERAL: the first two of base_insts.sail"
sed -n '1,75p' $M/model/extensions/I/base_insts.sail
sed -n '150,265p' $M/model/extensions/I/base_insts.sail
echo "[5/$total] config: how the model reads it, and the simulator's default file"
grep -rn 'config ' $M/model --include='*.sail' | wc -l
grep -rn 'config ' $M/model --include='*.sail' | head -8
ls $M/config 2>&1 | head
find / -name 'config*.json' -path '*sail*' -not -path '/proc/*' 2>/dev/null | head
sail_riscv_sim --help 2>&1 | grep -i -A1 'config' | head -12
echo "[6/$total] one whole-model typecheck, timed (the generator's fixed cost)"
cd $M/model
CFG=$(ls $M/config/*.json 2>/dev/null | head -1)
echo "config file: $CFG"
S=$(date +%s)
sail --project riscv.sail_project --all-modules --strict-var --strict-bitvector --strict-exponentials --just-check --memo-z3-path /work/sl1_smt_cache ${CFG:+--config $CFG} 2>&1 | tail -20
echo "  exit: $? seconds: $(( $(date +%s) - S ))"
echo "[7/$total] the softfloat externs (the float family's foreign interface), LITERAL"
grep -n '^val ' $M/model/core/softfloat_interface.sail | head -60
echo "done $(date -u +%FT%TZ)"
