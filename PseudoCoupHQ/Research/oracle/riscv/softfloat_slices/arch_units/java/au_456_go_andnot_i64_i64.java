// arch-unit 456  --  go  `a &^ b`  lhs=int64 rhs=int64
// symbol main.op_283   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   xori t6, a1, -0x1                    integer    operator:^
//   and a0, a0, t6                       integer    operator:&
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: int64, 64 bits.  parameters are operand bit patterns.
public final class au_456_go_andnot_i64_i64 {

    public static long au_456_go_andnot_i64_i64(long p0, long p1) {
        // a0: operand `a` (int64) arrives in a0
        final long v1 = p0;
        // a1: operand `b` (int64) arrives in a1
        final long v2 = p1;
        final long v3 = AuInt.au_xor(v2, 0xffffffffffffffffL);
        final long v4 = AuInt.au_and(v1, v3);
        // the answer is int64, 64 bits
        return v4;
    }
}
