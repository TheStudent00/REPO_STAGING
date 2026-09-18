// arch-unit 172  --  go  `a >= b`  lhs=float32 rhs=float32
// symbol main.op_657   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fle.s a0, fa1, fa0                 float    emulation:f32_le_rm0
//   jalr zero, 0x0(ra)                 integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
public final class au_172_go_ge_f32_f32 {
    public static long au_172_go_ge_f32_f32(long p0, long p1) {
    // fa0: operand `a` (float32) arrives in fa0
        final long v1 = ((p0) & 0xffffffffL);
    // fa1: operand `b` (float32) arrives in fa1
        final long v2 = ((p1) & 0xffffffffL);
        final long v3 = (f32_le.f32_le_rm0(v2, v1) ? 1L : 0L);
        return v3;
    }
}
