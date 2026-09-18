// arch-unit 354  --  c  `a | b`  lhs=uint64_t rhs=bool
// symbol op_371   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.or a0, a1                          integer    operator:|
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
public final class au_354_c_bor_u64_bool {

    public static long au_354_c_bor_u64_bool(long p0, long p1) {
        // a0: operand `a` (uint64_t) arrives in a0
        final long v1 = p0;
        // a1: operand `b` (bool) zero-extended to XLEN
        final long v2 = ((p1) & 0x1L);
        final long v3 = AuInt.au_or(v1, v2);
        // the answer is uint64_t, 64 bits
        return v3;
    }
}
