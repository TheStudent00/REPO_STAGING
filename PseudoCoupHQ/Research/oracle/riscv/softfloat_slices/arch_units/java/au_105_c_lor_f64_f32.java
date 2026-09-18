// arch-unit 105  --  c  `a || b`  lhs=double rhs=float
// symbol op_309   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fmv.d.x fa5, zero                  float    bit-manipulation
//   feq.d a0, fa0, fa5                 float    emulation:f64_eq_rm0
//   fmv.w.x fa5, zero                  float    bit-manipulation
//   feq.s a1, fa1, fa5                 float    emulation:f32_eq_rm0
//   c.and a0, a1                       integer  operator:&
//   xori a0, a0, 0x1                   integer  operator:^
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
public final class au_105_c_lor_f64_f32 {
    public static long au_105_c_lor_f64_f32(long p0, long p1) {
    // fa0: operand `a` (double) arrives in fa0
        final long v1 = p0;
    // fa1: operand `b` (float) arrives in fa1
        final long v2 = ((p1) & 0xffffffffL);
        final long v3 = 0x0L;
        final long v4 = (f64_eq.f64_eq_rm0(v1, v3) ? 1L : 0L);
        final long v5 = ((0x0L) & 0xffffffffL);
        final long v6 = (f32_eq.f32_eq_rm0(v2, v5) ? 1L : 0L);
        final long v7 = ((v4) & (v6));
        final long v8 = ((v7) ^ 0x1L);
        return v8;
    }
}
