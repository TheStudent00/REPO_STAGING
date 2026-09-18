// arch-unit 488  --  go  `a >= b`  lhs=int64 rhs=int64
// symbol main.op_643   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   slt t0, a0, a1                       integer    operator:< signed
//   sltiu a0, t0, 0x1                    integer    operator:< unsigned
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: bool, 1 bits.  parameters are operand bit patterns.
public final class au_488_go_ge_i64_i64 {

    public static long au_488_go_ge_i64_i64(long p0, long p1) {
        // a0: operand `a` (int64) arrives in a0
        final long v1 = p0;
        // a1: operand `b` (int64) arrives in a1
        final long v2 = p1;
        final long v3 = AuInt.au_slt(v1, v2);
        final long v4 = AuInt.au_sltu(v3, 0x1L);
        // the answer is bool, 1 bits
        return ((v4) & 0x1L);
    }
}
