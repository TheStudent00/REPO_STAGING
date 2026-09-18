// arch-unit 134  --  c  `a == b`  lhs=uint64_t rhs=float
// symbol op_477   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.lu fa5, a0, dyn             float    emulation:ui64_to_f32_rm0
//   feq.s a0, fa0, fa5                 float    emulation:f32_eq_rm0
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
public final class au_134_c_eq_u64_f32 {
    public static long au_134_c_eq_u64_f32(long p0, long p1) {
    // a0: operand `a` (uint64_t) arrives in a0
        final long v1 = p0;
    // fa0: operand `b` (float) arrives in fa0
        final long v2 = ((p1) & 0xffffffffL);
        final long v3 = ui64_to_f32.ui64_to_f32_rm0(v1);
        final long v4 = (f32_eq.f32_eq_rm0(v2, v3) ? 1L : 0L);
        return v4;
    }
}
