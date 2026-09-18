// arch-unit 416  --  go  `-a`  lhs=uint64 rhs=None
// symbol main.op_8   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sub a0, zero, a0                     integer    operator:-
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: uint64, 64 bits.  parameters are operand bit patterns.
public final class au_416_go_neg_u64 {

    public static long au_416_go_neg_u64(long p0) {
        // a0: operand `a` (uint64) arrives in a0
        final long v1 = p0;
        final long v2 = AuInt.au_sub(0x0L, v1);
        // the answer is uint64, 64 bits
        return v2;
    }
}
