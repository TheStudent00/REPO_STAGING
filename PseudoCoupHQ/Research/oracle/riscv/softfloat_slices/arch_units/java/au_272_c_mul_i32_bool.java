// arch-unit 272  --  c  `a * b`  lhs=int32_t rhs=bool
// symbol op_179   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   czero.eqz a0, a0, a1                 integer    conditional select
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
public final class au_272_c_mul_i32_bool {

    public static long au_272_c_mul_i32_bool(long p0, long p1) {
        // a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
        final long v1 = AuInt.au_sext32(p0);
        // a1: operand `b` (bool) zero-extended to XLEN
        final long v2 = ((p1) & 0x1L);
        final long v3 = AuInt.au_czeqz(v1, v2);
        // the answer is int32_t, 32 bits
        return ((v3) & 0xffffffffL);
    }
}
