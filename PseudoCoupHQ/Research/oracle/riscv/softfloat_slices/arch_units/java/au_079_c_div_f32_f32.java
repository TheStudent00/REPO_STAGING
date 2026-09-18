// arch-unit 79  --  c  `a / b`  lhs=float rhs=float
// symbol op_231   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fdiv.s fa0, fa0, fa1, dyn          float    emulation:f32_div_rm0
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
public final class au_079_c_div_f32_f32 {
    public static long au_079_c_div_f32_f32(long p0, long p1) {
    // fa0: operand `a` (float) arrives in fa0
        final long v1 = ((p0) & 0xffffffffL);
    // fa1: operand `b` (float) arrives in fa1
        final long v2 = ((p1) & 0xffffffffL);
        final long v3 = f32_div.f32_div_rm0(v1, v2);
        return ((v3) & 0xffffffffL);
    }
}
