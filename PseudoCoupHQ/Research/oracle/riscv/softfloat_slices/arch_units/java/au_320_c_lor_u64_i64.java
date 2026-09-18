// arch-unit 320  --  c  `a || b`  lhs=uint64_t rhs=int64_t
// symbol op_295   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.or a0, a1                          integer    operator:|
//   sltu a0, zero, a0                    integer    operator:< unsigned
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
public final class au_320_c_lor_u64_i64 {

    public static long au_320_c_lor_u64_i64(long p0, long p1) {
        // a0: operand `a` (uint64_t) arrives in a0
        final long v1 = p0;
        // a1: operand `b` (int64_t) arrives in a1
        final long v2 = p1;
        final long v3 = AuInt.au_or(v1, v2);
        final long v4 = AuInt.au_sltu(0x0L, v3);
        // the answer is int32_t, 32 bits
        return ((v4) & 0xffffffffL);
    }
}
