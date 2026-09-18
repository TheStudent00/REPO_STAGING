// arch-unit 175  --  c  `!a`  lhs=int64_t rhs=None
// symbol op_1   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltiu a0, a0, 0x1                    integer    operator:< unsigned
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
public final class au_175_c_not_i64 {

    public static long au_175_c_not_i64(long p0) {
        // a0: operand `a` (int64_t) arrives in a0
        final long v1 = p0;
        final long v2 = AuInt.au_sltu(v1, 0x1L);
        // the answer is int32_t, 32 bits
        return ((v2) & 0xffffffffL);
    }
}
