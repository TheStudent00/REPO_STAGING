// arch-unit 228  --  c  `a++`  lhs=int64_t rhs=None
// symbol op_91   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
public final class au_228_c_postinc_i64 {

    public static long au_228_c_postinc_i64(long p0) {
        // a0: operand `a` (int64_t) arrives in a0
        final long v1 = p0;
        // the answer is int64_t, 64 bits
        return v1;
    }
}
