// arch-unit 58  --  c  `a * b`  lhs=float rhs=uint64_t
// symbol op_194   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.lu fa5, a0, dyn             float    emulation:ui64_to_f32_rm0
//   fmul.s fa0, fa0, fa5, dyn          float    emulation:f32_mul_rm0
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
public final class au_058_c_mul_f32_u64 {
    public static long au_058_c_mul_f32_u64(long p0, long p1) {
    // fa0: operand `a` (float) arrives in fa0
        final long v1 = ((p0) & 0xffffffffL);
    // a0: operand `b` (uint64_t) arrives in a0
        final long v2 = p1;
        final long v3 = ui64_to_f32.ui64_to_f32_rm0(v2);
        final long v4 = f32_mul.f32_mul_rm0(v1, v3);
        return ((v4) & 0xffffffffL);
    }
}
