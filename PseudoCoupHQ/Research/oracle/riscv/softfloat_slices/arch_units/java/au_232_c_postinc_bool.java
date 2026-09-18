// arch-unit 232  --  c  `a++`  lhs=bool rhs=None
// symbol op_95   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: _Bool, 1 bits.  parameters are operand bit patterns.
public final class au_232_c_postinc_bool {

    public static long au_232_c_postinc_bool(long p0) {
        // a0: operand `a` (bool) zero-extended to XLEN
        final long v1 = ((p0) & 0x1L);
        // the answer is _Bool, 1 bits
        return ((v1) & 0x1L);
    }
}
