// arch-unit 192  --  c  `++a`  lhs=bool rhs=None
// symbol op_41   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.li a0, 0x1                         integer    constant
//   c.jr ra                              integer    return
//
// answer: _Bool, 1 bits.  parameters are operand bit patterns.
public final class au_192_c_preinc_bool {

    public static long au_192_c_preinc_bool(long p0) {
        // a0: operand `a` (bool) zero-extended to XLEN
        final long v1 = ((p0) & 0x1L);
        final long v2 = 0x1L;
        // the answer is _Bool, 1 bits
        return ((v2) & 0x1L);
    }
}
