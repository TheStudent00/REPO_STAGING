// arch-unit 2  --  c  `-a`  lhs=float rhs=None
// symbol op_15   outcome WALK_REFUSED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fsgnjn.s fa0, fa0, fa0             float    bit-manipulation
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
public final class au_002_c_neg_f32 {
    public static long au_002_c_neg_f32(long p0) {
    // fa0: operand `a` (float) arrives in fa0
        final long v1 = ((p0) & 0xffffffffL);
        final long v2 = (((v1) & 0x7fffffffL) | ((~(v1)) & 0x80000000L));
        return ((v2) & 0xffffffffL);
    }
}
