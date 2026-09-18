// arch-unit 170  --  go  `a > b`  lhs=float32 rhs=float32
// symbol main.op_621   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   flt.s a0, fa1, fa0                 float    emulation:f32_lt_rm0
//   jalr zero, 0x0(ra)                 integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
public final class au_170_go_gt_f32_f32 {
    public static long au_170_go_gt_f32_f32(long p0, long p1) {
    // fa0: operand `a` (float32) arrives in fa0
        final long v1 = ((p0) & 0xffffffffL);
    // fa1: operand `b` (float32) arrives in fa1
        final long v2 = ((p1) & 0xffffffffL);
        final long v3 = (f32_lt.f32_lt_rm0(v2, v1) ? 1L : 0L);
        return v3;
    }
}
