// arch-unit 55  --  c  `a * b`  lhs=uint64_t rhs=double
// symbol op_190   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.lu fa5, a0, dyn             float    emulation:ui64_to_f64_rm0
//   fmul.d fa0, fa0, fa5, dyn          float    emulation:f64_mul_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
public final class au_055_c_mul_u64_f64 {
    public static long au_055_c_mul_u64_f64(long p0, long p1) {
    // a0: operand `a` (uint64_t) arrives in a0
        final long v1 = p0;
    // fa0: operand `b` (double) arrives in fa0
        final long v2 = p1;
        final long v3 = ui64_to_f64.ui64_to_f64_rm0(v1);
        final long v4 = f64_mul.f64_mul_rm0(v2, v3);
        return v4;
    }
}
