// arch-unit 415  --  go  `-a`  lhs=int64 rhs=None
// symbol main.op_7   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sub a0, zero, a0                     integer    operator:-
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: int64, 64 bits.  parameters are operand bit patterns.
public final class au_415_go_neg_i64 {

    public static long au_415_go_neg_i64(long p0) {
        // a0: operand `a` (int64) arrives in a0
        final long v1 = p0;
        final long v2 = AuInt.au_sub(0x0L, v1);
        // the answer is int64, 64 bits
        return v2;
    }
}
