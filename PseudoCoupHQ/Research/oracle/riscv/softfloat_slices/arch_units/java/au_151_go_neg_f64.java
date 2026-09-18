// arch-unit 151  --  go  `-a`  lhs=float64 rhs=None
// symbol main.op_10   outcome WALK_REFUSED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fsgnjn.d fa0, fa0, fa0             float    bit-manipulation
//   jalr zero, 0x0(ra)                 integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
public final class au_151_go_neg_f64 {
    public static long au_151_go_neg_f64(long p0) {
    // fa0: operand `a` (float64) arrives in fa0
        final long v1 = p0;
        final long v2 = (((v1) & 0x7fffffffffffffffL) | ((~(v1)) & 0x8000000000000000L));
        return v2;
    }
}
