// arch-unit 385  --  c  `a & b`  lhs=uint64_t rhs=uint64_t
// symbol op_440   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.and a0, a1                         integer    operator:&
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
public final class au_385_c_band_u64_u64 {

    public static long au_385_c_band_u64_u64(long p0, long p1) {
        // a0: operand `a` (uint64_t) arrives in a0
        final long v1 = p0;
        // a1: operand `b` (uint64_t) arrives in a1
        final long v2 = p1;
        final long v3 = AuInt.au_and(v1, v2);
        // the answer is uint64_t, 64 bits
        return v3;
    }
}
