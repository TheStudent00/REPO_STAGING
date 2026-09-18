// arch-unit 148  --  c  `a == b`  lhs=bool rhs=float
// symbol op_495   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.wu fa5, a0, dyn             float    emulation:ui32_to_f32_rm0
//   feq.s a0, fa0, fa5                 float    emulation:f32_eq_rm0
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
public final class au_148_c_eq_bool_f32 {
    public static long au_148_c_eq_bool_f32(long p0, long p1) {
    // a0: operand `a` (bool) zero-extended
        final long v1 = ((p0) & 0x1L);
    // fa0: operand `b` (float) arrives in fa0
        final long v2 = ((p1) & 0xffffffffL);
        final long v3 = ui32_to_f32.ui32_to_f32_rm0(((int)((((v1) & 0xffffffffL)) & 0xffffffffL)));
        final long v4 = (f32_eq.f32_eq_rm0(v2, v3) ? 1L : 0L);
        return v4;
    }
}
