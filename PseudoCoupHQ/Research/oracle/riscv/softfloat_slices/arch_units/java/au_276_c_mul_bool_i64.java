// arch-unit 276  --  c  `a * b`  lhs=bool rhs=int64_t
// symbol op_205   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   czero.eqz a0, a1, a0                 integer    conditional select
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
public final class au_276_c_mul_bool_i64 {

    public static long au_276_c_mul_bool_i64(long p0, long p1) {
        // a0: operand `a` (bool) zero-extended to XLEN
        final long v1 = ((p0) & 0x1L);
        // a1: operand `b` (int64_t) arrives in a1
        final long v2 = p1;
        final long v3 = AuInt.au_czeqz(v2, v1);
        // the answer is int64_t, 64 bits
        return v3;
    }
}
