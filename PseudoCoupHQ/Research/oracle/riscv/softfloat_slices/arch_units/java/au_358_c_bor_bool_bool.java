// arch-unit 358  --  c  `a | b`  lhs=bool rhs=bool
// symbol op_389   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.or a0, a1                          integer    operator:|
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
public final class au_358_c_bor_bool_bool {

    public static long au_358_c_bor_bool_bool(long p0, long p1) {
        // a0: operand `a` (bool) zero-extended to XLEN
        final long v1 = ((p0) & 0x1L);
        // a1: operand `b` (bool) zero-extended to XLEN
        final long v2 = ((p1) & 0x1L);
        final long v3 = AuInt.au_or(v1, v2);
        // the answer is int32_t, 32 bits
        return ((v3) & 0xffffffffL);
    }
}
