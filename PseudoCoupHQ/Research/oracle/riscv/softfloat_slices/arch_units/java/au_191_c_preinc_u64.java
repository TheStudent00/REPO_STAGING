// arch-unit 191  --  c  `++a`  lhs=uint64_t rhs=None
// symbol op_38   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.addi a0, 0x1                       integer    operator:+
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
public final class au_191_c_preinc_u64 {

    public static long au_191_c_preinc_u64(long p0) {
        // a0: operand `a` (uint64_t) arrives in a0
        final long v1 = p0;
        final long v2 = AuInt.au_add(v1, 0x1L);
        // the answer is uint64_t, 64 bits
        return v2;
    }
}
