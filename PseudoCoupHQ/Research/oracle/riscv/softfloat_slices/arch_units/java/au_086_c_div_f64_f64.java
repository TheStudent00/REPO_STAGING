// arch-unit 86  --  c  `a / b`  lhs=double rhs=double
// symbol op_238   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fdiv.d fa0, fa0, fa1, dyn          float    emulation:f64_div_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
public final class au_086_c_div_f64_f64 {
    public static long au_086_c_div_f64_f64(long p0, long p1) {
    // fa0: operand `a` (double) arrives in fa0
        final long v1 = p0;
    // fa1: operand `b` (double) arrives in fa1
        final long v2 = p1;
        final long v3 = f64_div.f64_div_rm0(v1, v2);
        return v3;
    }
}
