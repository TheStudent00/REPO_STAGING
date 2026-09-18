// arch-unit 410  --  go  `+a`  lhs=int64 rhs=None
// symbol main.op_1   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: int64, 64 bits.  parameters are operand bit patterns.
public final class au_410_go_pos_i64 {

    public static long au_410_go_pos_i64(long p0) {
        // a0: operand `a` (int64) arrives in a0
        final long v1 = p0;
        // the answer is int64, 64 bits
        return v1;
    }
}
