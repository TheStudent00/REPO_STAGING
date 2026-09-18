// arch-unit 160  --  go  `a - b`  lhs=float32 rhs=float32
// symbol main.op_369   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fsub.s fa0, fa0, fa1, rne          float    emulation:f32_sub_rm0
//   jalr zero, 0x0(ra)                 integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
public final class au_160_go_neg_f32_f32 {
    public static long au_160_go_neg_f32_f32(long p0, long p1) {
    // fa0: operand `a` (float32) arrives in fa0
        final long v1 = ((p0) & 0xffffffffL);
    // fa1: operand `b` (float32) arrives in fa1
        final long v2 = ((p1) & 0xffffffffL);
        final long v3 = f32_sub.f32_sub_rm0(v1, v2);
        return ((v3) & 0xffffffffL);
    }
}
