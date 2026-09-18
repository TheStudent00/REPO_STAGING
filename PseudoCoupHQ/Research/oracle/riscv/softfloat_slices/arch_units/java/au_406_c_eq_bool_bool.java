// arch-unit 406  --  c  `a == b`  lhs=bool rhs=bool
// symbol op_497   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.xor a0, a1                         integer    operator:^
//   xori a0, a0, 0x1                     integer    operator:^
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
public final class au_406_c_eq_bool_bool {

    public static long au_406_c_eq_bool_bool(long p0, long p1) {
        // a0: operand `a` (bool) zero-extended to XLEN
        final long v1 = ((p0) & 0x1L);
        // a1: operand `b` (bool) zero-extended to XLEN
        final long v2 = ((p1) & 0x1L);
        final long v3 = AuInt.au_xor(v1, v2);
        final long v4 = AuInt.au_xor(v3, 0x1L);
        // the answer is int32_t, 32 bits
        return ((v4) & 0xffffffffL);
    }
}
