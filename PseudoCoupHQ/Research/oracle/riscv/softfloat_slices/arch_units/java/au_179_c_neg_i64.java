// arch-unit 179  --  c  `-a`  lhs=int64_t rhs=None
// symbol op_13   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sub a0, zero, a0                     integer    operator:-
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
public final class au_179_c_neg_i64 {

    public static long au_179_c_neg_i64(long p0) {
        // a0: operand `a` (int64_t) arrives in a0
        final long v1 = p0;
        final long v2 = AuInt.au_sub(0x0L, v1);
        // the answer is int64_t, 64 bits
        return v2;
    }
}
