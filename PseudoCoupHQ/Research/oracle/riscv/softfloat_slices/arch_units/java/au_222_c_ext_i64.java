// arch-unit 222  --  c  `__extension__ a`  lhs=int64_t rhs=None
// symbol op_85   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
public final class au_222_c_ext_i64 {

    public static long au_222_c_ext_i64(long p0) {
        // a0: operand `a` (int64_t) arrives in a0
        final long v1 = p0;
        // the answer is int64_t, 64 bits
        return v1;
    }
}
