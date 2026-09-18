# arch-unit 155  --  go  `a * b`  lhs=float64 rhs=float64
# symbol main.op_88   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fmul.d fa0, fa0, fa1, rne          float    emulation:f64_mul_rm0
#   jalr zero, 0x0(ra)                 integer  return
#
# answer: f64, 64 bits.  parameters are operand bit patterns.
from au_float import *        # noqa: F401,F403

def au_155_go_mul_f64_f64(p0, p1):
    # fa0: operand `a` (float64) arrives in fa0
    v1 = p0
    # fa1: operand `b` (float64) arrives in fa1
    v2 = p1
    v3 = f64_mul_rm0(v1, v2)
    return v3
