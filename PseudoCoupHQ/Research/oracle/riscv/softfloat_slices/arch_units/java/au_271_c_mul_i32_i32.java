// arch-unit 271  --  c  `a * b`  lhs=int32_t rhs=int32_t
// symbol op_174   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   mulw a0, a1, a0                      integer    operator:* then sign-extend the low 32 bits
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
public final class au_271_c_mul_i32_i32 {

    public static long au_271_c_mul_i32_i32(long p0, long p1) {
        // a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
        final long v1 = AuInt.au_sext32(p0);
        // a1: operand `b` (int32_t) sign-extended to XLEN, as the ABI presents it
        final long v2 = AuInt.au_sext32(p1);
        final long v3 = AuInt.au_mulw(v2, v1);
        // the answer is int32_t, 32 bits
        return ((v3) & 0xffffffffL);
    }
}
