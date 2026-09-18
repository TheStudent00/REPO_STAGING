// arch-unit 268  --  c  `a - b`  lhs=bool rhs=int64_t
// symbol op_169   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.sub a0, a1                         integer    operator:-
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
public final class au_268_c_sub_bool_i64 {

    public static long au_268_c_sub_bool_i64(long p0, long p1) {
        // a0: operand `a` (bool) zero-extended to XLEN
        final long v1 = ((p0) & 0x1L);
        // a1: operand `b` (int64_t) arrives in a1
        final long v2 = p1;
        final long v3 = AuInt.au_sub(v1, v2);
        // the answer is int64_t, 64 bits
        return v3;
    }
}
