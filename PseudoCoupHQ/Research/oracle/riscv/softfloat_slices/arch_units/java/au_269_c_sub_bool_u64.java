// arch-unit 269  --  c  `a - b`  lhs=bool rhs=uint64_t
// symbol op_170   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.sub a0, a1                         integer    operator:-
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
public final class au_269_c_sub_bool_u64 {

    public static long au_269_c_sub_bool_u64(long p0, long p1) {
        // a0: operand `a` (bool) zero-extended to XLEN
        final long v1 = ((p0) & 0x1L);
        // a1: operand `b` (uint64_t) arrives in a1
        final long v2 = p1;
        final long v3 = AuInt.au_sub(v1, v2);
        // the answer is uint64_t, 64 bits
        return v3;
    }
}
