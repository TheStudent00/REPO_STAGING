# arch-unit 21  --  c  `a + b`  lhs=float rhs=bool
# symbol op_125   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fcvt.s.wu fa5, a0, dyn             float    emulation:ui32_to_f32_rm0
#   fadd.s fa0, fa0, fa5, dyn          float    emulation:f32_add_rm0
#   c.jr ra                            integer  return
#
# answer: f32, 32 bits.  parameters are operand bit patterns.
from au_float import *        # noqa: F401,F403

def au_021_c_add_f32_bool(p0, p1):
    # fa0: operand `a` (float) arrives in fa0
    v1 = ((p0) & 0xffffffff)
    # a0: operand `b` (bool) zero-extended
    v2 = ((p1) & 0x1)
    v3 = ui32_to_f32_rm0(((v2) & 0xffffffff))
    v4 = f32_add_rm0(v1, v3)
    return ((v4) & 0xffffffff)
