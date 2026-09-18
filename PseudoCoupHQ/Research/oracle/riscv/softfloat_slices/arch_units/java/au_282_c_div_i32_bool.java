// arch-unit 282  --  c  `a / b`  lhs=int32_t rhs=bool
// symbol op_215   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
public final class au_282_c_div_i32_bool {

    public static long au_282_c_div_i32_bool(long p0, long p1) {
        // a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
        final long v1 = AuInt.au_sext32(p0);
        // a1: operand `b` (bool) zero-extended to XLEN
        final long v2 = ((p1) & 0x1L);
        // the answer is int32_t, 32 bits
        return ((v1) & 0xffffffffL);
    }
}
