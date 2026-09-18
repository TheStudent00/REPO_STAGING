// arch-unit 136  --  c  `a == b`  lhs=float rhs=int32_t
// symbol op_480   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.w fa5, a0, dyn              float    emulation:i32_to_f32_rm0
//   feq.s a0, fa0, fa5                 float    emulation:f32_eq_rm0
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
public final class au_136_c_eq_f32_i32 {
    public static long au_136_c_eq_f32_i32(long p0, long p1) {
    // fa0: operand `a` (float) arrives in fa0
        final long v1 = ((p0) & 0xffffffffL);
    // a0: operand `b` (int32_t) sign-extended to XLEN
        final long v2 = ((long)(int)(p1));
        final long v3 = i32_to_f32.i32_to_f32_rm0(((int)((((v2) & 0xffffffffL)) & 0xffffffffL)));
        final long v4 = (f32_eq.f32_eq_rm0(v1, v3) ? 1L : 0L);
        return v4;
    }
}
