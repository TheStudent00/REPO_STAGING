// arch-unit 314  --  c  `a || b`  lhs=int32_t rhs=bool
// symbol op_287   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltu a0, zero, a0                    integer    operator:< unsigned
//   c.or a0, a1                          integer    operator:|
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
public final class au_314_c_lor_i32_bool {

    public static long au_314_c_lor_i32_bool(long p0, long p1) {
        // a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
        final long v1 = AuInt.au_sext32(p0);
        // a1: operand `b` (bool) zero-extended to XLEN
        final long v2 = ((p1) & 0x1L);
        final long v3 = AuInt.au_sltu(0x0L, v1);
        final long v4 = AuInt.au_or(v3, v2);
        // the answer is int32_t, 32 bits
        return ((v4) & 0xffffffffL);
    }
}
