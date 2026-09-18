// arch-unit 461  --  go  `a - b`  lhs=int32 rhs=int32
// symbol main.op_348   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.sub a0, a1                         integer    operator:-
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: int32, 32 bits.  parameters are operand bit patterns.
public final class au_461_go_sub_i32_i32 {

    public static long au_461_go_sub_i32_i32(long p0, long p1) {
        // a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
        final long v1 = AuInt.au_sext32(p0);
        // a1: operand `b` (int32) sign-extended to XLEN, as the ABI presents it
        final long v2 = AuInt.au_sext32(p1);
        final long v3 = AuInt.au_sub(v1, v2);
        // the answer is int32, 32 bits
        return ((v3) & 0xffffffffL);
    }
}
