// arch-unit 181  --  c  `-a`  lhs=bool rhs=None
// symbol op_17   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sub a0, zero, a0                     integer    operator:-
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
public final class au_181_c_neg_bool {

    public static long au_181_c_neg_bool(long p0) {
        // a0: operand `a` (bool) zero-extended to XLEN
        final long v1 = ((p0) & 0x1L);
        final long v2 = AuInt.au_sub(0x0L, v1);
        // the answer is int32_t, 32 bits
        return ((v2) & 0xffffffffL);
    }
}
