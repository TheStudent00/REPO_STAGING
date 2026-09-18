// arch-unit 109  --  c  `a || b`  lhs=bool rhs=double
// symbol op_316   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fmv.d.x fa5, zero                  float    bit-manipulation
//   feq.d a1, fa0, fa5                 float    emulation:f64_eq_rm0
//   xori a1, a1, 0x1                   integer  operator:^
//   c.or a0, a1                        integer  operator:|
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
public final class au_109_c_lor_bool_f64 {
    public static long au_109_c_lor_bool_f64(long p0, long p1) {
    // a0: operand `a` (bool) zero-extended
        final long v1 = ((p0) & 0x1L);
    // fa0: operand `b` (double) arrives in fa0
        final long v2 = p1;
        final long v3 = 0x0L;
        final long v4 = (f64_eq.f64_eq_rm0(v2, v3) ? 1L : 0L);
        final long v5 = ((v4) ^ 0x1L);
        final long v6 = ((v1) | (v5));
        return v6;
    }
}
