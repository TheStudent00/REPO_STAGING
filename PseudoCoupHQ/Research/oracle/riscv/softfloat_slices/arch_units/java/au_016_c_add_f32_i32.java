// arch-unit 16  --  c  `a + b`  lhs=float rhs=int32_t
// symbol op_120   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.w fa5, a0, dyn              float    emulation:i32_to_f32_rm0
//   fadd.s fa0, fa0, fa5, dyn          float    emulation:f32_add_rm0
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
public final class au_016_c_add_f32_i32 {
    public static long au_016_c_add_f32_i32(long p0, long p1) {
    // fa0: operand `a` (float) arrives in fa0
        final long v1 = ((p0) & 0xffffffffL);
    // a0: operand `b` (int32_t) sign-extended to XLEN
        final long v2 = ((long)(int)(p1));
        final long v3 = i32_to_f32.i32_to_f32_rm0(((int)((((v2) & 0xffffffffL)) & 0xffffffffL)));
        final long v4 = f32_add.f32_add_rm0(v1, v3);
        return ((v4) & 0xffffffffL);
    }
}
