// arch-unit 491  --  go  `a || b`  lhs=bool rhs=bool
// symbol main.op_743   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.or a0, a1                          integer    operator:|
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: bool, 1 bits.  parameters are operand bit patterns.
public final class au_491_go_lor_bool_bool {

    public static long au_491_go_lor_bool_bool(long p0, long p1) {
        // a0: operand `a` (bool) zero-extended to XLEN
        final long v1 = ((p0) & 0x1L);
        // a1: operand `b` (bool) zero-extended to XLEN
        final long v2 = ((p1) & 0x1L);
        final long v3 = AuInt.au_or(v1, v2);
        // the answer is bool, 1 bits
        return ((v3) & 0x1L);
    }
}
