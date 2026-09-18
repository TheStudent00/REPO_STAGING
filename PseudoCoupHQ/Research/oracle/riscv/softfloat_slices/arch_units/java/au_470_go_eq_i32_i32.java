// arch-unit 470  --  go  `a == b`  lhs=int32 rhs=int32
// symbol main.op_456   outcome LIFTED   5 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   addiw t0, a0, 0x0                    integer    operator:+ then sign-extend the low 32 bits
//   addiw t1, a1, 0x0                    integer    operator:+ then sign-extend the low 32 bits
//   sub t0, t0, t1                       integer    operator:-
//   sltiu a0, t0, 0x1                    integer    operator:< unsigned
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: bool, 1 bits.  parameters are operand bit patterns.
public final class au_470_go_eq_i32_i32 {

    public static long au_470_go_eq_i32_i32(long p0, long p1) {
        // a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
        final long v1 = AuInt.au_sext32(p0);
        // a1: operand `b` (int32) sign-extended to XLEN, as the ABI presents it
        final long v2 = AuInt.au_sext32(p1);
        final long v3 = AuInt.au_addw(v1, 0x0L);
        final long v4 = AuInt.au_addw(v2, 0x0L);
        final long v5 = AuInt.au_sub(v3, v4);
        final long v6 = AuInt.au_sltu(v5, 0x1L);
        // the answer is bool, 1 bits
        return ((v6) & 0x1L);
    }
}
