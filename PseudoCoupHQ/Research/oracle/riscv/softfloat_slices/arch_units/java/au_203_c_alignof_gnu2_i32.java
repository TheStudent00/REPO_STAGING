// arch-unit 203  --  c  `__alignof__ a`  lhs=int32_t rhs=None
// symbol op_54   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.li a0, 0x4                         integer    constant
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
public final class au_203_c_alignof_gnu2_i32 {

    public static long au_203_c_alignof_gnu2_i32(long p0) {
        // a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
        final long v1 = AuInt.au_sext32(p0);
        final long v2 = 0x4L;
        // the answer is uint64_t, 64 bits
        return v2;
    }
}
