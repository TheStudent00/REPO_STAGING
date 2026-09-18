// arch-unit 88  --  c  `a / b`  lhs=bool rhs=float
// symbol op_243   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.wu fa5, a0, dyn             float    emulation:ui32_to_f32_rm0
//   fdiv.s fa0, fa5, fa0, dyn          float    emulation:f32_div_rm0
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
public final class au_088_c_div_bool_f32 {
    public static long au_088_c_div_bool_f32(long p0, long p1) {
    // a0: operand `a` (bool) zero-extended
        final long v1 = ((p0) & 0x1L);
    // fa0: operand `b` (float) arrives in fa0
        final long v2 = ((p1) & 0xffffffffL);
        final long v3 = ui32_to_f32.ui32_to_f32_rm0(((int)((((v1) & 0xffffffffL)) & 0xffffffffL)));
        final long v4 = f32_div.f32_div_rm0(v3, v2);
        return ((v4) & 0xffffffffL);
    }
}
