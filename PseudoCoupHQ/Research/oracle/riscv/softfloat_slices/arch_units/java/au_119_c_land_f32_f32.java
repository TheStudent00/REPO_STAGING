// arch-unit 119  --  c  `a && b`  lhs=float rhs=float
// symbol op_339   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fmv.w.x fa5, zero                  float    bit-manipulation
//   feq.s a0, fa0, fa5                 float    emulation:f32_eq_rm0
//   feq.s a1, fa1, fa5                 float    emulation:f32_eq_rm0
//   c.or a0, a1                        integer  operator:|
//   xori a0, a0, 0x1                   integer  operator:^
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
public final class au_119_c_land_f32_f32 {
    public static long au_119_c_land_f32_f32(long p0, long p1) {
    // fa0: operand `a` (float) arrives in fa0
        final long v1 = ((p0) & 0xffffffffL);
    // fa1: operand `b` (float) arrives in fa1
        final long v2 = ((p1) & 0xffffffffL);
        final long v3 = ((0x0L) & 0xffffffffL);
        final long v4 = (f32_eq.f32_eq_rm0(v1, v3) ? 1L : 0L);
        final long v5 = (f32_eq.f32_eq_rm0(v2, v3) ? 1L : 0L);
        final long v6 = ((v4) | (v5));
        final long v7 = ((v6) ^ 0x1L);
        return v7;
    }
}
