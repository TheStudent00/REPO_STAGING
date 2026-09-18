// arch-unit 77  --  c  `a / b`  lhs=float rhs=int64_t
// symbol op_229   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.l fa5, a0, dyn              float    emulation:i64_to_f32_rm0
//   fdiv.s fa0, fa0, fa5, dyn          float    emulation:f32_div_rm0
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
public final class au_077_c_div_f32_i64 {
    public static long au_077_c_div_f32_i64(long p0, long p1) {
    // fa0: operand `a` (float) arrives in fa0
        final long v1 = ((p0) & 0xffffffffL);
    // a0: operand `b` (int64_t) arrives in a0
        final long v2 = p1;
        final long v3 = i64_to_f32.i64_to_f32_rm0(v2);
        final long v4 = f32_div.f32_div_rm0(v1, v3);
        return ((v4) & 0xffffffffL);
    }
}
