// arch-unit 279  --  c  `a / b`  lhs=int32_t rhs=int32_t
// symbol op_210   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   divw a0, a0, a1                      integer    written-out restoring division (NOT the language's /)
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
public final class au_279_c_div_i32_i32 {

    public static long au_279_c_div_i32_i32(long p0, long p1) {
        // a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
        final long v1 = AuInt.au_sext32(p0);
        // a1: operand `b` (int32_t) sign-extended to XLEN, as the ABI presents it
        final long v2 = AuInt.au_sext32(p1);
        final long v3 = AuInt.au_divw(v1, v2);
        // the answer is int32_t, 32 bits
        return ((v3) & 0xffffffffL);
    }
}
