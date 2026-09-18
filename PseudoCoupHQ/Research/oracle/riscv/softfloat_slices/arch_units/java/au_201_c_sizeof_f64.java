// arch-unit 201  --  c  `sizeof a`  lhs=double rhs=None
// symbol op_52   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.li a0, 0x8                         integer    constant
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
public final class au_201_c_sizeof_f64 {

    public static long au_201_c_sizeof_f64(long p0) {
        // fa0: operand `a` (double) arrives in fa0 as a bit pattern
        final long v1 = p0;
        final long v2 = 0x8L;
        // the answer is uint64_t, 64 bits
        return v2;
    }
}
