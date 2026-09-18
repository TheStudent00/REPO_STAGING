// arch-unit 463  --  go  `a - b`  lhs=uint64 rhs=uint64
// symbol main.op_362   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.sub a0, a1                         integer    operator:-
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: uint64, 64 bits.  parameters are operand bit patterns.
public final class au_463_go_sub_u64_u64 {

    public static long au_463_go_sub_u64_u64(long p0, long p1) {
        // a0: operand `a` (uint64) arrives in a0
        final long v1 = p0;
        // a1: operand `b` (uint64) arrives in a1
        final long v2 = p1;
        final long v3 = AuInt.au_sub(v1, v2);
        // the answer is uint64, 64 bits
        return v3;
    }
}
