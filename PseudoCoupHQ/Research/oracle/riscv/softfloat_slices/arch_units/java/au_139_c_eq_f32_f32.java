// arch-unit 139  --  c  `a == b`  lhs=float rhs=float
// symbol op_483   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   feq.s a0, fa0, fa1                 float    emulation:f32_eq_rm0
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
public final class au_139_c_eq_f32_f32 {
    public static long au_139_c_eq_f32_f32(long p0, long p1) {
    // fa0: operand `a` (float) arrives in fa0
        final long v1 = ((p0) & 0xffffffffL);
    // fa1: operand `b` (float) arrives in fa1
        final long v2 = ((p1) & 0xffffffffL);
        final long v3 = (f32_eq.f32_eq_rm0(v1, v2) ? 1L : 0L);
        return v3;
    }
}
