// arch-unit 468  --  go  `a ^ b`  lhs=int64 rhs=int64
// symbol main.op_427   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.xor a0, a1                         integer    operator:^
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: int64, 64 bits.  parameters are operand bit patterns.
public final class au_468_go_bxor_i64_i64 {

    public static long au_468_go_bxor_i64_i64(long p0, long p1) {
        // a0: operand `a` (int64) arrives in a0
        final long v1 = p0;
        // a1: operand `b` (int64) arrives in a1
        final long v2 = p1;
        final long v3 = AuInt.au_xor(v1, v2);
        // the answer is int64, 64 bits
        return v3;
    }
}
