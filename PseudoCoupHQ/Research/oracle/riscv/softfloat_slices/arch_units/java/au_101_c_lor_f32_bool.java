// arch-unit 101  --  c  `a || b`  lhs=float rhs=bool
// symbol op_305   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fmv.w.x fa5, zero                  float    bit-manipulation
//   feq.s a1, fa0, fa5                 float    emulation:f32_eq_rm0
//   xori a1, a1, 0x1                   integer  operator:^
//   c.or a0, a1                        integer  operator:|
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
public final class au_101_c_lor_f32_bool {
    public static long au_101_c_lor_f32_bool(long p0, long p1) {
    // fa0: operand `a` (float) arrives in fa0
        final long v1 = ((p0) & 0xffffffffL);
    // a0: operand `b` (bool) zero-extended
        final long v2 = ((p1) & 0x1L);
        final long v3 = ((0x0L) & 0xffffffffL);
        final long v4 = (f32_eq.f32_eq_rm0(v1, v3) ? 1L : 0L);
        final long v5 = ((v4) ^ 0x1L);
        final long v6 = ((v2) | (v5));
        return v6;
    }
}
