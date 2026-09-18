// arch-unit 3  --  c  `-a`  lhs=double rhs=None
// symbol op_16   outcome WALK_REFUSED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fsgnjn.d fa0, fa0, fa0             float    bit-manipulation
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
public final class au_003_c_neg_f64 {
    public static long au_003_c_neg_f64(long p0) {
    // fa0: operand `a` (double) arrives in fa0
        final long v1 = p0;
        final long v2 = (((v1) & 0x7fffffffffffffffL) | ((~(v1)) & 0x8000000000000000L));
        return v2;
    }
}
