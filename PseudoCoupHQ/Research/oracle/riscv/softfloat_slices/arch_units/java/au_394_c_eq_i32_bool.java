// arch-unit 394  --  c  `a == b`  lhs=int32_t rhs=bool
// symbol op_467   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.xor a0, a1                         integer    operator:^
//   sltiu a0, a0, 0x1                    integer    operator:< unsigned
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
public final class au_394_c_eq_i32_bool {

    public static long au_394_c_eq_i32_bool(long p0, long p1) {
        // a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
        final long v1 = AuInt.au_sext32(p0);
        // a1: operand `b` (bool) zero-extended to XLEN
        final long v2 = ((p1) & 0x1L);
        final long v3 = AuInt.au_xor(v1, v2);
        final long v4 = AuInt.au_sltu(v3, 0x1L);
        // the answer is int32_t, 32 bits
        return ((v4) & 0xffffffffL);
    }
}
