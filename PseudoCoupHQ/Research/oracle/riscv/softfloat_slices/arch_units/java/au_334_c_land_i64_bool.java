// arch-unit 334  --  c  `a && b`  lhs=int64_t rhs=bool
// symbol op_329   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltu a0, zero, a0                    integer    operator:< unsigned
//   c.and a0, a1                         integer    operator:&
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
public final class au_334_c_land_i64_bool {

    public static long au_334_c_land_i64_bool(long p0, long p1) {
        // a0: operand `a` (int64_t) arrives in a0
        final long v1 = p0;
        // a1: operand `b` (bool) zero-extended to XLEN
        final long v2 = ((p1) & 0x1L);
        final long v3 = AuInt.au_sltu(0x0L, v1);
        final long v4 = AuInt.au_and(v3, v2);
        // the answer is int32_t, 32 bits
        return ((v4) & 0xffffffffL);
    }
}
