// arch-unit 304  --  c  `a % b`  lhs=uint64_t rhs=int64_t
// symbol op_259   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   remu a0, a0, a1                      integer    written-out restoring division (NOT the language's %)
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
public final class au_304_c_rem_u64_i64 {

    public static long au_304_c_rem_u64_i64(long p0, long p1) {
        // a0: operand `a` (uint64_t) arrives in a0
        final long v1 = p0;
        // a1: operand `b` (int64_t) arrives in a1
        final long v2 = p1;
        final long v3 = AuInt.au_remu(v1, v2);
        // the answer is uint64_t, 64 bits
        return v3;
    }
}
