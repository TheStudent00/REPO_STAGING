// arch-unit 0  --  c  `!a`  lhs=float rhs=None
// symbol op_3   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fmv.w.x fa5, zero                  float    bit-manipulation
//   feq.s a0, fa0, fa5                 float    emulation:f32_eq_rm0
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
public final class au_000_c_not_f32 {
    public static long au_000_c_not_f32(long p0) {
    // fa0: operand `a` (float) arrives in fa0
        final long v1 = ((p0) & 0xffffffffL);
        final long v2 = ((0x0L) & 0xffffffffL);
        final long v3 = (f32_eq.f32_eq_rm0(v1, v2) ? 1L : 0L);
        return v3;
    }
}
