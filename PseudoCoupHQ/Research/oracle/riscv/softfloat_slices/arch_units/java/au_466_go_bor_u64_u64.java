// arch-unit 466  --  go  `a | b`  lhs=uint64 rhs=uint64
// symbol main.op_398   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.or a0, a1                          integer    operator:|
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: uint64, 64 bits.  parameters are operand bit patterns.
public final class au_466_go_bor_u64_u64 {

    public static long au_466_go_bor_u64_u64(long p0, long p1) {
        // a0: operand `a` (uint64) arrives in a0
        final long v1 = p0;
        // a1: operand `b` (uint64) arrives in a1
        final long v2 = p1;
        final long v3 = AuInt.au_or(v1, v2);
        // the answer is uint64, 64 bits
        return v3;
    }
}
