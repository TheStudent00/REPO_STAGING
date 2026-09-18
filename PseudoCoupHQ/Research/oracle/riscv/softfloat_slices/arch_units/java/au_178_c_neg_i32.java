// arch-unit 178  --  c  `-a`  lhs=int32_t rhs=None
// symbol op_12   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   subw a0, zero, a0                    integer    operator:- then sign-extend the low 32 bits
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
public final class au_178_c_neg_i32 {

    public static long au_178_c_neg_i32(long p0) {
        // a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
        final long v1 = AuInt.au_sext32(p0);
        final long v2 = AuInt.au_subw(0x0L, v1);
        // the answer is int32_t, 32 bits
        return ((v2) & 0xffffffffL);
    }
}
