// arch-unit 277  --  c  `a * b`  lhs=bool rhs=uint64_t
// symbol op_206   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   czero.eqz a0, a1, a0                 integer    conditional select
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
public final class au_277_c_mul_bool_u64 {

    public static long au_277_c_mul_bool_u64(long p0, long p1) {
        // a0: operand `a` (bool) zero-extended to XLEN
        final long v1 = ((p0) & 0x1L);
        // a1: operand `b` (uint64_t) arrives in a1
        final long v2 = p1;
        final long v3 = AuInt.au_czeqz(v2, v1);
        // the answer is uint64_t, 64 bits
        return v3;
    }
}
