// arch-unit 49  --  c  `a - b`  lhs=bool rhs=double
// symbol op_172   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.wu fa5, a0                  float    emulation:ui32_to_f64_rm0
//   fsub.d fa0, fa5, fa0, dyn          float    emulation:f64_sub_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
public final class au_049_c_neg_bool_f64 {
    public static long au_049_c_neg_bool_f64(long p0, long p1) {
    // a0: operand `a` (bool) zero-extended
        final long v1 = ((p0) & 0x1L);
    // fa0: operand `b` (double) arrives in fa0
        final long v2 = p1;
        final long v3 = ui32_to_f64.ui32_to_f64_rm0(((int)((((v1) & 0xffffffffL)) & 0xffffffffL)));
        final long v4 = f64_sub.f64_sub_rm0(v3, v2);
        return v4;
    }
}
