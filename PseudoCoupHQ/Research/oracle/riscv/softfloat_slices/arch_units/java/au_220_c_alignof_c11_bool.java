// arch-unit 220  --  c  `_Alignof a`  lhs=bool rhs=None
// symbol op_83   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.li a0, 0x1                         integer    constant
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
public final class au_220_c_alignof_c11_bool {

    public static long au_220_c_alignof_c11_bool(long p0) {
        // a0: operand `a` (bool) zero-extended to XLEN
        final long v1 = ((p0) & 0x1L);
        final long v2 = 0x1L;
        // the answer is uint64_t, 64 bits
        return v2;
    }
}
