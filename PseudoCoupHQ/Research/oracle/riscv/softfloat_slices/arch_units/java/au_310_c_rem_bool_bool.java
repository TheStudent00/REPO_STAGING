// arch-unit 310  --  c  `a % b`  lhs=bool rhs=bool
// symbol op_281   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.li a0, 0x0                         integer    constant
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
public final class au_310_c_rem_bool_bool {

    public static long au_310_c_rem_bool_bool(long p0, long p1) {
        // a0: operand `a` (bool) zero-extended to XLEN
        final long v1 = ((p0) & 0x1L);
        // a1: operand `b` (bool) zero-extended to XLEN
        final long v2 = ((p1) & 0x1L);
        final long v3 = 0x0L;
        // the answer is int32_t, 32 bits
        return ((v3) & 0xffffffffL);
    }
}
