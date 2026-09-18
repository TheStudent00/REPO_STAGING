// arch-unit 294  --  c  `a / b`  lhs=bool rhs=bool
// symbol op_245   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
public final class au_294_c_div_bool_bool {

    public static long au_294_c_div_bool_bool(long p0, long p1) {
        // a0: operand `a` (bool) zero-extended to XLEN
        final long v1 = ((p0) & 0x1L);
        // a1: operand `b` (bool) zero-extended to XLEN
        final long v2 = ((p1) & 0x1L);
        // the answer is int32_t, 32 bits
        return ((v1) & 0xffffffffL);
    }
}
