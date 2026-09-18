// arch-unit 98  --  c  `a || b`  lhs=float rhs=uint64_t
// symbol op_302   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fmv.w.x fa5, zero                  float    bit-manipulation
//   feq.s a1, fa0, fa5                 float    emulation:f32_eq_rm0
//   xori a1, a1, 0x1                   integer  operator:^
//   sltu a0, zero, a0                  integer  operator:<
//   c.or a0, a1                        integer  operator:|
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
public final class au_098_c_lor_f32_u64 {
    public static long au_098_c_lor_f32_u64(long p0, long p1) {
    // fa0: operand `a` (float) arrives in fa0
        final long v1 = ((p0) & 0xffffffffL);
    // a0: operand `b` (uint64_t) arrives in a0
        final long v2 = p1;
        final long v3 = ((0x0L) & 0xffffffffL);
        final long v4 = (f32_eq.f32_eq_rm0(v1, v3) ? 1L : 0L);
        final long v5 = ((v4) ^ 0x1L);
        final long v6 = (Long.compareUnsigned(0x0L, v2) < 0 ? 1L : 0L);
        final long v7 = ((v6) | (v5));
        return v7;
    }
}
