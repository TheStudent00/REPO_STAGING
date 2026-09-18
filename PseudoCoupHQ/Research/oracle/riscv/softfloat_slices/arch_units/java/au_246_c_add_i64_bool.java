// arch-unit 246  --  c  `a + b`  lhs=int64_t rhs=bool
// symbol op_113   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.add a0, a1                         integer    operator:+
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
public final class au_246_c_add_i64_bool {

    public static long au_246_c_add_i64_bool(long p0, long p1) {
        // a0: operand `a` (int64_t) arrives in a0
        final long v1 = p0;
        // a1: operand `b` (bool) zero-extended to XLEN
        final long v2 = ((p1) & 0x1L);
        final long v3 = AuInt.au_add(v1, v2);
        // the answer is int64_t, 64 bits
        return v3;
    }
}
