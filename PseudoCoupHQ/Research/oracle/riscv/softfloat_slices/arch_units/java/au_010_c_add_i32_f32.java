// arch-unit 10  --  c  `a + b`  lhs=int32_t rhs=float
// symbol op_105   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.w fa5, a0, dyn              float    emulation:i32_to_f32_rm0
//   fadd.s fa0, fa0, fa5, dyn          float    emulation:f32_add_rm0
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
public final class au_010_c_add_i32_f32 {
    public static long au_010_c_add_i32_f32(long p0, long p1) {
    // a0: operand `a` (int32_t) sign-extended to XLEN
        final long v1 = ((long)(int)(p0));
    // fa0: operand `b` (float) arrives in fa0
        final long v2 = ((p1) & 0xffffffffL);
        final long v3 = i32_to_f32.i32_to_f32_rm0(((int)((((v1) & 0xffffffffL)) & 0xffffffffL)));
        final long v4 = f32_add.f32_add_rm0(v2, v3);
        return ((v4) & 0xffffffffL);
    }
}
