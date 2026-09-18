// arch-unit 13  --  c  `a + b`  lhs=int64_t rhs=double
// symbol op_112   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.l fa5, a0, dyn              float    emulation:i64_to_f64_rm0
//   fadd.d fa0, fa0, fa5, dyn          float    emulation:f64_add_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
public final class au_013_c_add_i64_f64 {
    public static long au_013_c_add_i64_f64(long p0, long p1) {
    // a0: operand `a` (int64_t) arrives in a0
        final long v1 = p0;
    // fa0: operand `b` (double) arrives in fa0
        final long v2 = p1;
        final long v3 = i64_to_f64.i64_to_f64_rm0(v1);
        final long v4 = f64_add.f64_add_rm0(v2, v3);
        return v4;
    }
}
