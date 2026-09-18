// arch-unit 476  --  go  `a != b`  lhs=uint64 rhs=uint64
// symbol main.op_506   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sub t0, a0, a1                       integer    operator:-
//   sltu a0, zero, t0                    integer    operator:< unsigned
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: bool, 1 bits.  parameters are operand bit patterns.
public final class au_476_go_ne_u64_u64 {

    public static long au_476_go_ne_u64_u64(long p0, long p1) {
        // a0: operand `a` (uint64) arrives in a0
        final long v1 = p0;
        // a1: operand `b` (uint64) arrives in a1
        final long v2 = p1;
        final long v3 = AuInt.au_sub(v1, v2);
        final long v4 = AuInt.au_sltu(0x0L, v3);
        // the answer is bool, 1 bits
        return ((v4) & 0x1L);
    }
}
