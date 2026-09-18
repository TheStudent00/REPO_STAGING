# arch-unit 95  --  c  `a || b`  lhs=uint64_t rhs=double
# symbol op_298   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   sltu a0, zero, a0                  integer  operator:<
#   fmv.d.x fa5, zero                  float    bit-manipulation
#   feq.d a1, fa0, fa5                 float    emulation:f64_eq_rm0
#   xori a1, a1, 0x1                   integer  operator:^
#   c.or a0, a1                        integer  operator:|
#   c.jr ra                            integer  return
#
# answer: int, 64 bits.  parameters are operand bit patterns.
from au_float import *        # noqa: F401,F403

def au_095_c_lor_u64_f64(p0, p1):
    # a0: operand `a` (uint64_t) arrives in a0
    v1 = p0
    # fa0: operand `b` (double) arrives in fa0
    v2 = p1
    v3 = (1 if (0x0) < (v1) else 0)
    v4 = 0x0
    v5 = f64_eq_rm0(v2, v4)
    v6 = ((v5) ^ 0x1)
    v7 = ((v3) | (v6))
    return v7
