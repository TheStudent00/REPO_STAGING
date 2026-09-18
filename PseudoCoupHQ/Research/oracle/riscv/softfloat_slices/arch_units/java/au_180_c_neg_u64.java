// arch-unit 180  --  c  `-a`  lhs=uint64_t rhs=None
// symbol op_14   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sub a0, zero, a0                     integer    operator:-
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
public final class au_180_c_neg_u64 {

    public static long au_180_c_neg_u64(long p0) {
        // a0: operand `a` (uint64_t) arrives in a0
        final long v1 = p0;
        final long v2 = AuInt.au_sub(0x0L, v1);
        // the answer is uint64_t, 64 bits
        return v2;
    }
}
