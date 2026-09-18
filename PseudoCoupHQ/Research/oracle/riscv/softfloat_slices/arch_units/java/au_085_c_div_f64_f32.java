// arch-unit 85  --  c  `a / b`  lhs=double rhs=float
// symbol op_237   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.s fa5, fa1                  float    emulation:f32_to_f64_rm0
//   fdiv.d fa0, fa0, fa5, dyn          float    emulation:f64_div_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
public final class au_085_c_div_f64_f32 {
    public static long au_085_c_div_f64_f32(long p0, long p1) {
    // fa0: operand `a` (double) arrives in fa0
        final long v1 = p0;
    // fa1: operand `b` (float) arrives in fa1
        final long v2 = ((p1) & 0xffffffffL);
        final long v3 = f32_to_f64.f32_to_f64_rm0(v2);
        final long v4 = f64_div.f64_div_rm0(v1, v3);
        return v4;
    }
}
