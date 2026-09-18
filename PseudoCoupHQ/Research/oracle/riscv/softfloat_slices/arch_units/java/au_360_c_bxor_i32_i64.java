// arch-unit 360  --  c  `a ^ b`  lhs=int32_t rhs=int64_t
// symbol op_391   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.xor a0, a1                         integer    operator:^
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
public final class au_360_c_bxor_i32_i64 {

    public static long au_360_c_bxor_i32_i64(long p0, long p1) {
        // a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
        final long v1 = AuInt.au_sext32(p0);
        // a1: operand `b` (int64_t) arrives in a1
        final long v2 = p1;
        final long v3 = AuInt.au_xor(v1, v2);
        // the answer is int64_t, 64 bits
        return v3;
    }
}
