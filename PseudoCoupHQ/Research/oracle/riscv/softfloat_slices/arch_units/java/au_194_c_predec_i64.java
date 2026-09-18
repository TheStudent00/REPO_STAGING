// arch-unit 194  --  c  `--a`  lhs=int64_t rhs=None
// symbol op_43   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.addi a0, -0x1                      integer    operator:+
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
public final class au_194_c_predec_i64 {

    public static long au_194_c_predec_i64(long p0) {
        // a0: operand `a` (int64_t) arrives in a0
        final long v1 = p0;
        final long v2 = AuInt.au_add(v1, 0xffffffffffffffffL);
        // the answer is int64_t, 64 bits
        return v2;
    }
}
