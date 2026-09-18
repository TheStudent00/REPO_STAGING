// arch-unit 174  --  c  `!a`  lhs=int32_t rhs=None
// symbol op_0   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltiu a0, a0, 0x1                    integer    operator:< unsigned
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
public final class au_174_c_not_i32 {

    public static long au_174_c_not_i32(long p0) {
        // a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
        final long v1 = AuInt.au_sext32(p0);
        final long v2 = AuInt.au_sltu(v1, 0x1L);
        // the answer is int32_t, 32 bits
        return ((v2) & 0xffffffffL);
    }
}
