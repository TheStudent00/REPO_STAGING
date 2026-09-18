// arch-unit 161  --  go  `a - b`  lhs=float64 rhs=float64
// symbol main.op_376   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fsub.d fa0, fa0, fa1, rne          float    emulation:f64_sub_rm0
//   jalr zero, 0x0(ra)                 integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
public final class au_161_go_neg_f64_f64 {
    public static long au_161_go_neg_f64_f64(long p0, long p1) {
    // fa0: operand `a` (float64) arrives in fa0
        final long v1 = p0;
    // fa1: operand `b` (float64) arrives in fa1
        final long v2 = p1;
        final long v3 = f64_sub.f64_sub_rm0(v1, v2);
        return v3;
    }
}
