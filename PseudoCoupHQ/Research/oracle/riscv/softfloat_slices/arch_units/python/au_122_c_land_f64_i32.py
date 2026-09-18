# arch-unit 122  --  c  `a && b`  lhs=double rhs=int32_t
# symbol op_342   outcome WALK_REFUSED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fmv.d.x fa5, zero                  float    bit-manipulation
#   feq.d a1, fa0, fa5                 float    emulation:f64_eq_rm0
#   sltu a0, zero, a0                  integer  operator:<
#   andn a0, a0, a1                    integer  operator:& ~
#   c.jr ra                            integer  return
#
# answer: int, 64 bits.  parameters are operand bit patterns.
from au_float import *        # noqa: F401,F403

def au_122_c_land_f64_i32(p0, p1):
    # fa0: operand `a` (double) arrives in fa0
    v1 = p0
    # a0: operand `b` (int32_t) sign-extended to XLEN
    v2 = (((((p1) & 0xffffffff) ^ 0x80000000) - 0x80000000) & 0xffffffffffffffff)
    v3 = 0x0
    v4 = f64_eq_rm0(v1, v3)
    v5 = (1 if (0x0) < (v2) else 0)
    v6 = ((v5) & ((~(v4)) & 0xffffffffffffffff))
    return v6
