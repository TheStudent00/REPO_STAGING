// arch-unit 31  --  c  `a - b`  lhs=int32_t rhs=double
// symbol op_142   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.w fa5, a0                   float    emulation:i32_to_f64_rm0
//   fsub.d fa0, fa5, fa0, dyn          float    emulation:f64_sub_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
public final class au_031_c_neg_i32_f64 {
    public static long au_031_c_neg_i32_f64(long p0, long p1) {
    // a0: operand `a` (int32_t) sign-extended to XLEN
        final long v1 = ((long)(int)(p0));
    // fa0: operand `b` (double) arrives in fa0
        final long v2 = p1;
        final long v3 = i32_to_f64.i32_to_f64_rm0(((int)((((v1) & 0xffffffffL)) & 0xffffffffL)));
        final long v4 = f64_sub.f64_sub_rm0(v3, v2);
        return v4;
    }
}
