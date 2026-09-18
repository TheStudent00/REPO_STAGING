// arch-unit 242  --  c  `a + b`  lhs=int32_t rhs=bool
// symbol op_107   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.addw a0, a1                        integer    operator:+ then sign-extend the low 32 bits
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
public final class au_242_c_add_i32_bool {

    public static long au_242_c_add_i32_bool(long p0, long p1) {
        // a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
        final long v1 = AuInt.au_sext32(p0);
        // a1: operand `b` (bool) zero-extended to XLEN
        final long v2 = ((p1) & 0x1L);
        final long v3 = AuInt.au_addw(v1, v2);
        // the answer is int32_t, 32 bits
        return ((v3) & 0xffffffffL);
    }
}
