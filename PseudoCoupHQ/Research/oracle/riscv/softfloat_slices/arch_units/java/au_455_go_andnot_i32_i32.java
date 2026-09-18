// arch-unit 455  --  go  `a &^ b`  lhs=int32 rhs=int32
// symbol main.op_276   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   xori t6, a1, -0x1                    integer    operator:^
//   and a0, a0, t6                       integer    operator:&
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: int32, 32 bits.  parameters are operand bit patterns.
public final class au_455_go_andnot_i32_i32 {

    public static long au_455_go_andnot_i32_i32(long p0, long p1) {
        // a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
        final long v1 = AuInt.au_sext32(p0);
        // a1: operand `b` (int32) sign-extended to XLEN, as the ABI presents it
        final long v2 = AuInt.au_sext32(p1);
        final long v3 = AuInt.au_xor(v2, 0xffffffffffffffffL);
        final long v4 = AuInt.au_and(v1, v3);
        // the answer is int32, 32 bits
        return ((v4) & 0xffffffffL);
    }
}
