// arch-unit 396  --  c  `a == b`  lhs=int64_t rhs=int64_t
// symbol op_469   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.xor a0, a1                         integer    operator:^
//   sltiu a0, a0, 0x1                    integer    operator:< unsigned
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
public final class au_396_c_eq_i64_i64 {

    public static long au_396_c_eq_i64_i64(long p0, long p1) {
        // a0: operand `a` (int64_t) arrives in a0
        final long v1 = p0;
        // a1: operand `b` (int64_t) arrives in a1
        final long v2 = p1;
        final long v3 = AuInt.au_xor(v1, v2);
        final long v4 = AuInt.au_sltu(v3, 0x1L);
        // the answer is int32_t, 32 bits
        return ((v4) & 0xffffffffL);
    }
}
