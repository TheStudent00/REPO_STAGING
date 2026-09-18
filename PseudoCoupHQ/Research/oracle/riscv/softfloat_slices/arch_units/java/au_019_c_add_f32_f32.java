// arch-unit 19  --  c  `a + b`  lhs=float rhs=float
// symbol op_123   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fadd.s fa0, fa0, fa1, dyn          float    emulation:f32_add_rm0
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
public final class au_019_c_add_f32_f32 {
    public static long au_019_c_add_f32_f32(long p0, long p1) {
    // fa0: operand `a` (float) arrives in fa0
        final long v1 = ((p0) & 0xffffffffL);
    // fa1: operand `b` (float) arrives in fa1
        final long v2 = ((p1) & 0xffffffffL);
        final long v3 = f32_add.f32_add_rm0(v1, v2);
        return ((v3) & 0xffffffffL);
    }
}
