// arch-unit 61  --  c  `a * b`  lhs=float rhs=bool
// symbol op_197   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.wu fa5, a0, dyn             float    emulation:ui32_to_f32_rm0
//   fmul.s fa0, fa0, fa5, dyn          float    emulation:f32_mul_rm0
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
public final class au_061_c_mul_f32_bool {
    public static long au_061_c_mul_f32_bool(long p0, long p1) {
    // fa0: operand `a` (float) arrives in fa0
        final long v1 = ((p0) & 0xffffffffL);
    // a0: operand `b` (bool) zero-extended
        final long v2 = ((p1) & 0x1L);
        final long v3 = ui32_to_f32.ui32_to_f32_rm0(((int)((((v2) & 0xffffffffL)) & 0xffffffffL)));
        final long v4 = f32_mul.f32_mul_rm0(v1, v3);
        return ((v4) & 0xffffffffL);
    }
}
