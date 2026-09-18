// arch-unit 339  --  c  `a && b`  lhs=bool rhs=int32_t
// symbol op_348   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltu a1, zero, a1                    integer    operator:< unsigned
//   c.and a0, a1                         integer    operator:&
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
public final class au_339_c_land_bool_i32 {

    public static long au_339_c_land_bool_i32(long p0, long p1) {
        // a0: operand `a` (bool) zero-extended to XLEN
        final long v1 = ((p0) & 0x1L);
        // a1: operand `b` (int32_t) sign-extended to XLEN, as the ABI presents it
        final long v2 = AuInt.au_sext32(p1);
        final long v3 = AuInt.au_sltu(0x0L, v2);
        final long v4 = AuInt.au_and(v1, v3);
        // the answer is int32_t, 32 bits
        return ((v4) & 0xffffffffL);
    }
}
