// arch-unit 409  --  go  `+a`  lhs=int32 rhs=None
// symbol main.op_0   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: int32, 32 bits.  parameters are operand bit patterns.
public final class au_409_go_pos_i32 {

    public static long au_409_go_pos_i32(long p0) {
        // a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
        final long v1 = AuInt.au_sext32(p0);
        // the answer is int32, 32 bits
        return ((v1) & 0xffffffffL);
    }
}
