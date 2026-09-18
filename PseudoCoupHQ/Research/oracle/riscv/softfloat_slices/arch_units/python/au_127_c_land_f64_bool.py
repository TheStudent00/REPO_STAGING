# arch-unit 127  --  c  `a && b`  lhs=double rhs=bool
# symbol op_347   outcome WALK_REFUSED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fmv.d.x fa5, zero                  float    bit-manipulation
#   feq.d a1, fa0, fa5                 float    emulation:f64_eq_rm0
#   andn a0, a0, a1                    integer  operator:& ~
#   c.jr ra                            integer  return
#
# answer: int, 64 bits.  parameters are operand bit patterns.
from au_float import *        # noqa: F401,F403

def au_127_c_land_f64_bool(p0, p1):
    # fa0: operand `a` (double) arrives in fa0
    v1 = p0
    # a0: operand `b` (bool) zero-extended
    v2 = ((p1) & 0x1)
    v3 = 0x0
    v4 = f64_eq_rm0(v1, v3)
    v5 = ((v2) & ((~(v4)) & 0xffffffffffffffff))
    return v5
