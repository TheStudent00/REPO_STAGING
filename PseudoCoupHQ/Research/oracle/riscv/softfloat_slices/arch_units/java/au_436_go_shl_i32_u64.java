// arch-unit 436  --  go  `a << b`  lhs=int32 rhs=uint64
// symbol main.op_170   outcome LIFTED   5 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sll t0, a0, a1                       integer    operator:<< (count masked to 6 bits)
//   sltiu t1, a1, 0x40                   integer    operator:< unsigned
//   sub t1, zero, t1                     integer    operator:-
//   and a0, t0, t1                       integer    operator:&
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: int32, 32 bits.  parameters are operand bit patterns.
public final class au_436_go_shl_i32_u64 {

    public static long au_436_go_shl_i32_u64(long p0, long p1) {
        // a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
        final long v1 = AuInt.au_sext32(p0);
        // a1: operand `b` (uint64) arrives in a1
        final long v2 = p1;
        final long v3 = AuInt.au_sll(v1, v2);
        final long v4 = AuInt.au_sltu(v2, 0x40L);
        final long v5 = AuInt.au_sub(0x0L, v4);
        final long v6 = AuInt.au_and(v3, v5);
        // the answer is int32, 32 bits
        return ((v6) & 0xffffffffL);
    }
}
