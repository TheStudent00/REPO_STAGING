// arch-unit 164  --  go  `a != b`  lhs=float32 rhs=float32
// symbol main.op_513   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   feq.s a0, fa0, fa1                 float    emulation:f32_eq_rm0
//   xori a0, a0, 0x1                   integer  operator:^
//   jalr zero, 0x0(ra)                 integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
public final class au_164_go_ne_f32_f32 {
    public static long au_164_go_ne_f32_f32(long p0, long p1) {
    // fa0: operand `a` (float32) arrives in fa0
        final long v1 = ((p0) & 0xffffffffL);
    // fa1: operand `b` (float32) arrives in fa1
        final long v2 = ((p1) & 0xffffffffL);
        final long v3 = (f32_eq.f32_eq_rm0(v1, v2) ? 1L : 0L);
        final long v4 = ((v3) ^ 0x1L);
        return v4;
    }
}
