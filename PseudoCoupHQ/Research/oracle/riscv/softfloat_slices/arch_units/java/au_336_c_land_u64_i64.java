// arch-unit 336  --  c  `a && b`  lhs=uint64_t rhs=int64_t
// symbol op_331   outcome LIFTED   4 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltu a0, zero, a0                    integer    operator:< unsigned
//   sltu a1, zero, a1                    integer    operator:< unsigned
//   c.and a0, a1                         integer    operator:&
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
public final class au_336_c_land_u64_i64 {

    public static long au_336_c_land_u64_i64(long p0, long p1) {
        // a0: operand `a` (uint64_t) arrives in a0
        final long v1 = p0;
        // a1: operand `b` (int64_t) arrives in a1
        final long v2 = p1;
        final long v3 = AuInt.au_sltu(0x0L, v1);
        final long v4 = AuInt.au_sltu(0x0L, v2);
        final long v5 = AuInt.au_and(v3, v4);
        // the answer is int32_t, 32 bits
        return ((v5) & 0xffffffffL);
    }
}
