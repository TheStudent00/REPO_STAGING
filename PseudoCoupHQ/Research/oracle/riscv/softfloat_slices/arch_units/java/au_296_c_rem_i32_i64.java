// arch-unit 296  --  c  `a % b`  lhs=int32_t rhs=int64_t
// symbol op_247   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   rem a0, a0, a1                       integer    written-out restoring division (NOT the language's %)
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
public final class au_296_c_rem_i32_i64 {

    public static long au_296_c_rem_i32_i64(long p0, long p1) {
        // a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
        final long v1 = AuInt.au_sext32(p0);
        // a1: operand `b` (int64_t) arrives in a1
        final long v2 = p1;
        final long v3 = AuInt.au_rem(v1, v2);
        // the answer is int64_t, 64 bits
        return v3;
    }
}
