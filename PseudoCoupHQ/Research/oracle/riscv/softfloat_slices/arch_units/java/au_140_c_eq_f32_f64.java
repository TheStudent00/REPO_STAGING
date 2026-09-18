// arch-unit 140  --  c  `a == b`  lhs=float rhs=double
// symbol op_484   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.s fa5, fa0                  float    emulation:f32_to_f64_rm0
//   feq.d a0, fa1, fa5                 float    emulation:f64_eq_rm0
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
public final class au_140_c_eq_f32_f64 {
    public static long au_140_c_eq_f32_f64(long p0, long p1) {
    // fa0: operand `a` (float) arrives in fa0
        final long v1 = ((p0) & 0xffffffffL);
    // fa1: operand `b` (double) arrives in fa1
        final long v2 = p1;
        final long v3 = f32_to_f64.f32_to_f64_rm0(v1);
        final long v4 = (f64_eq.f64_eq_rm0(v2, v3) ? 1L : 0L);
        return v4;
    }
}
