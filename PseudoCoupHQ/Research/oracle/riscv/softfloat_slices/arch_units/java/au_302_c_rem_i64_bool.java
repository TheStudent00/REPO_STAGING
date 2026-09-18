// arch-unit 302  --  c  `a % b`  lhs=int64_t rhs=bool
// symbol op_257   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.li a0, 0x0                         integer    constant
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
public final class au_302_c_rem_i64_bool {

    public static long au_302_c_rem_i64_bool(long p0, long p1) {
        // a0: operand `a` (int64_t) arrives in a0
        final long v1 = p0;
        // a1: operand `b` (bool) zero-extended to XLEN
        final long v2 = ((p1) & 0x1L);
        final long v3 = 0x0L;
        // the answer is int64_t, 64 bits
        return v3;
    }
}
