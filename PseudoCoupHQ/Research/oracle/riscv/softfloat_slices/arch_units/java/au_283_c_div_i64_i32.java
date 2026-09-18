// arch-unit 283  --  c  `a / b`  lhs=int64_t rhs=int32_t
// symbol op_216   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   div a0, a0, a1                       integer    written-out restoring division (NOT the language's /)
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
public final class au_283_c_div_i64_i32 {

    public static long au_283_c_div_i64_i32(long p0, long p1) {
        // a0: operand `a` (int64_t) arrives in a0
        final long v1 = p0;
        // a1: operand `b` (int32_t) sign-extended to XLEN, as the ABI presents it
        final long v2 = AuInt.au_sext32(p1);
        final long v3 = AuInt.au_div(v1, v2);
        // the answer is int64_t, 64 bits
        return v3;
    }
}
