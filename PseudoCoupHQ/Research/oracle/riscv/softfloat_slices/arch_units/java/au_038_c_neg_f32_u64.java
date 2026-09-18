// arch-unit 38  --  c  `a - b`  lhs=float rhs=uint64_t
// symbol op_158   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.lu fa5, a0, dyn             float    emulation:ui64_to_f32_rm0
//   fsub.s fa0, fa0, fa5, dyn          float    emulation:f32_sub_rm0
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
public final class au_038_c_neg_f32_u64 {
    public static long au_038_c_neg_f32_u64(long p0, long p1) {
    // fa0: operand `a` (float) arrives in fa0
        final long v1 = ((p0) & 0xffffffffL);
    // a0: operand `b` (uint64_t) arrives in a0
        final long v2 = p1;
        final long v3 = ui64_to_f32.ui64_to_f32_rm0(v2);
        final long v4 = f32_sub.f32_sub_rm0(v1, v3);
        return ((v4) & 0xffffffffL);
    }
}
