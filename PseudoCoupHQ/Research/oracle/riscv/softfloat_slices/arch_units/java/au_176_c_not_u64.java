// arch-unit 176  --  c  `!a`  lhs=uint64_t rhs=None
// symbol op_2   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltiu a0, a0, 0x1                    integer    operator:< unsigned
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
public final class au_176_c_not_u64 {

    public static long au_176_c_not_u64(long p0) {
        // a0: operand `a` (uint64_t) arrives in a0
        final long v1 = p0;
        final long v2 = AuInt.au_sltu(v1, 0x1L);
        // the answer is int32_t, 32 bits
        return ((v2) & 0xffffffffL);
    }
}
