// arch-unit 211  --  c  `__alignof a`  lhs=uint64_t rhs=None
// symbol op_62   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.li a0, 0x8                         integer    constant
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
public final class au_211_c_alignof_gnu_u64 {

    public static long au_211_c_alignof_gnu_u64(long p0) {
        // a0: operand `a` (uint64_t) arrives in a0
        final long v1 = p0;
        final long v2 = 0x8L;
        // the answer is uint64_t, 64 bits
        return v2;
    }
}
