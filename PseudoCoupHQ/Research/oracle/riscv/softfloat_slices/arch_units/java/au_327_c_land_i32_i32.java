// arch-unit 327  --  c  `a && b`  lhs=int32_t rhs=int32_t
// symbol op_318   outcome LIFTED   4 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltu a0, zero, a0                    integer    operator:< unsigned
//   sltu a1, zero, a1                    integer    operator:< unsigned
//   c.and a0, a1                         integer    operator:&
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
public final class au_327_c_land_i32_i32 {

    public static long au_327_c_land_i32_i32(long p0, long p1) {
        // a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
        final long v1 = AuInt.au_sext32(p0);
        // a1: operand `b` (int32_t) sign-extended to XLEN, as the ABI presents it
        final long v2 = AuInt.au_sext32(p1);
        final long v3 = AuInt.au_sltu(0x0L, v1);
        final long v4 = AuInt.au_sltu(0x0L, v2);
        final long v5 = AuInt.au_and(v3, v4);
        // the answer is int32_t, 32 bits
        return ((v5) & 0xffffffffL);
    }
}
