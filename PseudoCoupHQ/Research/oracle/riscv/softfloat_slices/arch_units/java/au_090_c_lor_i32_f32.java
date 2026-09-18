// arch-unit 90  --  c  `a || b`  lhs=int32_t rhs=float
// symbol op_285   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltu a0, zero, a0                  integer  operator:<
//   fmv.w.x fa5, zero                  float    bit-manipulation
//   feq.s a1, fa0, fa5                 float    emulation:f32_eq_rm0
//   xori a1, a1, 0x1                   integer  operator:^
//   c.or a0, a1                        integer  operator:|
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
public final class au_090_c_lor_i32_f32 {
    public static long au_090_c_lor_i32_f32(long p0, long p1) {
    // a0: operand `a` (int32_t) sign-extended to XLEN
        final long v1 = ((long)(int)(p0));
    // fa0: operand `b` (float) arrives in fa0
        final long v2 = ((p1) & 0xffffffffL);
        final long v3 = (Long.compareUnsigned(0x0L, v1) < 0 ? 1L : 0L);
        final long v4 = ((0x0L) & 0xffffffffL);
        final long v5 = (f32_eq.f32_eq_rm0(v2, v4) ? 1L : 0L);
        final long v6 = ((v5) ^ 0x1L);
        final long v7 = ((v3) | (v6));
        return v7;
    }
}
