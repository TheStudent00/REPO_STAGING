// arch-unit 402  --  c  `a == b`  lhs=uint64_t rhs=bool
// symbol op_479   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.xor a0, a1                         integer    operator:^
//   sltiu a0, a0, 0x1                    integer    operator:< unsigned
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
public final class au_402_c_eq_u64_bool {

    public static long au_402_c_eq_u64_bool(long p0, long p1) {
        // a0: operand `a` (uint64_t) arrives in a0
        final long v1 = p0;
        // a1: operand `b` (bool) zero-extended to XLEN
        final long v2 = ((p1) & 0x1L);
        final long v3 = AuInt.au_xor(v1, v2);
        final long v4 = AuInt.au_sltu(v3, 0x1L);
        // the answer is int32_t, 32 bits
        return ((v4) & 0xffffffffL);
    }
}
