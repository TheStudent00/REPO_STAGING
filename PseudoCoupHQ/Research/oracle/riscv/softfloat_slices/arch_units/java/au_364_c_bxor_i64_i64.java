// arch-unit 364  --  c  `a ^ b`  lhs=int64_t rhs=int64_t
// symbol op_397   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.xor a0, a1                         integer    operator:^
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
public final class au_364_c_bxor_i64_i64 {

    public static long au_364_c_bxor_i64_i64(long p0, long p1) {
        // a0: operand `a` (int64_t) arrives in a0
        final long v1 = p0;
        // a1: operand `b` (int64_t) arrives in a1
        final long v2 = p1;
        final long v3 = AuInt.au_xor(v1, v2);
        // the answer is int64_t, 64 bits
        return v3;
    }
}
