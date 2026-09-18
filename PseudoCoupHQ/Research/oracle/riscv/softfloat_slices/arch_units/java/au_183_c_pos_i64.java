// arch-unit 183  --  c  `+a`  lhs=int64_t rhs=None
// symbol op_19   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
public final class au_183_c_pos_i64 {

    public static long au_183_c_pos_i64(long p0) {
        // a0: operand `a` (int64_t) arrives in a0
        final long v1 = p0;
        // the answer is int64_t, 64 bits
        return v1;
    }
}
