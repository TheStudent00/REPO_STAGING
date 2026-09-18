// arch-unit 486  --  go  `a > b`  lhs=uint64 rhs=uint64
// symbol main.op_614   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltu a0, a1, a0                      integer    operator:< unsigned
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: bool, 1 bits.  parameters are operand bit patterns.
public final class au_486_go_gt_u64_u64 {

    public static long au_486_go_gt_u64_u64(long p0, long p1) {
        // a0: operand `a` (uint64) arrives in a0
        final long v1 = p0;
        // a1: operand `b` (uint64) arrives in a1
        final long v2 = p1;
        final long v3 = AuInt.au_sltu(v2, v1);
        // the answer is bool, 1 bits
        return ((v3) & 0x1L);
    }
}
