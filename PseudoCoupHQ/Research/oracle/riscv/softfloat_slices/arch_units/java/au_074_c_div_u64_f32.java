// arch-unit 74  --  c  `a / b`  lhs=uint64_t rhs=float
// symbol op_225   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.lu fa5, a0, dyn             float    emulation:ui64_to_f32_rm0
//   fdiv.s fa0, fa5, fa0, dyn          float    emulation:f32_div_rm0
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
public final class au_074_c_div_u64_f32 {
    public static long au_074_c_div_u64_f32(long p0, long p1) {
    // a0: operand `a` (uint64_t) arrives in a0
        final long v1 = p0;
    // fa0: operand `b` (float) arrives in fa0
        final long v2 = ((p1) & 0xffffffffL);
        final long v3 = ui64_to_f32.ui64_to_f32_rm0(v1);
        final long v4 = f32_div.f32_div_rm0(v3, v2);
        return ((v4) & 0xffffffffL);
    }
}
