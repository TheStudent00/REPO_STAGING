// arch-unit 367  --  c  `a ^ b`  lhs=uint64_t rhs=int32_t
// symbol op_402   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.xor a0, a1                         integer    operator:^
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
public final class au_367_c_bxor_u64_i32 {

    public static long au_367_c_bxor_u64_i32(long p0, long p1) {
        // a0: operand `a` (uint64_t) arrives in a0
        final long v1 = p0;
        // a1: operand `b` (int32_t) sign-extended to XLEN, as the ABI presents it
        final long v2 = AuInt.au_sext32(p1);
        final long v3 = AuInt.au_xor(v1, v2);
        // the answer is uint64_t, 64 bits
        return v3;
    }
}
