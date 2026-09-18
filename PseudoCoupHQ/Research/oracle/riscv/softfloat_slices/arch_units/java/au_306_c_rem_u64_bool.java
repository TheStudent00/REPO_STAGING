// arch-unit 306  --  c  `a % b`  lhs=uint64_t rhs=bool
// symbol op_263   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.li a0, 0x0                         integer    constant
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
public final class au_306_c_rem_u64_bool {

    public static long au_306_c_rem_u64_bool(long p0, long p1) {
        // a0: operand `a` (uint64_t) arrives in a0
        final long v1 = p0;
        // a1: operand `b` (bool) zero-extended to XLEN
        final long v2 = ((p1) & 0x1L);
        final long v3 = 0x0L;
        // the answer is uint64_t, 64 bits
        return v3;
    }
}
