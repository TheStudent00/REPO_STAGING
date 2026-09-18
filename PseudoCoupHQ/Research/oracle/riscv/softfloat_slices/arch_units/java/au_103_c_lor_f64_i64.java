// arch-unit 103  --  c  `a || b`  lhs=double rhs=int64_t
// symbol op_307   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fmv.d.x fa5, zero                  float    bit-manipulation
//   feq.d a1, fa0, fa5                 float    emulation:f64_eq_rm0
//   xori a1, a1, 0x1                   integer  operator:^
//   sltu a0, zero, a0                  integer  operator:<
//   c.or a0, a1                        integer  operator:|
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
public final class au_103_c_lor_f64_i64 {
    public static long au_103_c_lor_f64_i64(long p0, long p1) {
    // fa0: operand `a` (double) arrives in fa0
        final long v1 = p0;
    // a0: operand `b` (int64_t) arrives in a0
        final long v2 = p1;
        final long v3 = 0x0L;
        final long v4 = (f64_eq.f64_eq_rm0(v1, v3) ? 1L : 0L);
        final long v5 = ((v4) ^ 0x1L);
        final long v6 = (Long.compareUnsigned(0x0L, v2) < 0 ? 1L : 0L);
        final long v7 = ((v6) | (v5));
        return v7;
    }
}
