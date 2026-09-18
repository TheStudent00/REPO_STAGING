// arch-unit 146  --  c  `a == b`  lhs=double rhs=double
// symbol op_490   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   feq.d a0, fa0, fa1                 float    emulation:f64_eq_rm0
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
public final class au_146_c_eq_f64_f64 {
    public static long au_146_c_eq_f64_f64(long p0, long p1) {
    // fa0: operand `a` (double) arrives in fa0
        final long v1 = p0;
    // fa1: operand `b` (double) arrives in fa1
        final long v2 = p1;
        final long v3 = (f64_eq.f64_eq_rm0(v1, v2) ? 1L : 0L);
        return v3;
    }
}
