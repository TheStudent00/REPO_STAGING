// arch-unit 54  --  c  `a * b`  lhs=uint64_t rhs=float
// symbol op_189   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.lu fa5, a0, dyn             float    emulation:ui64_to_f32_rm0
//   fmul.s fa0, fa0, fa5, dyn          float    emulation:f32_mul_rm0
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
public final class au_054_c_mul_u64_f32 {
    public static long au_054_c_mul_u64_f32(long p0, long p1) {
    // a0: operand `a` (uint64_t) arrives in a0
        final long v1 = p0;
    // fa0: operand `b` (float) arrives in fa0
        final long v2 = ((p1) & 0xffffffffL);
        final long v3 = ui64_to_f32.ui64_to_f32_rm0(v1);
        final long v4 = f32_mul.f32_mul_rm0(v2, v3);
        return ((v4) & 0xffffffffL);
    }
}
