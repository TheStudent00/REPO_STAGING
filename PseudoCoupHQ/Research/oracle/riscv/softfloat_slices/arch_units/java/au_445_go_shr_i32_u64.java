// arch-unit 445  --  go  `a >> b`  lhs=int32 rhs=uint64
// symbol main.op_206   outcome LIFTED   5 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltiu t0, a1, 0x20                   integer    operator:< unsigned
//   c.addi t0, -0x1                      integer    operator:+
//   or t0, a1, t0                        integer    operator:|
//   sraw a0, a0, t0                      integer    arithmetic right shift of the low 32 bits, written out
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: int32, 32 bits.  parameters are operand bit patterns.
public final class au_445_go_shr_i32_u64 {

    public static long au_445_go_shr_i32_u64(long p0, long p1) {
        // a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
        final long v1 = AuInt.au_sext32(p0);
        // a1: operand `b` (uint64) arrives in a1
        final long v2 = p1;
        final long v3 = AuInt.au_sltu(v2, 0x20L);
        final long v4 = AuInt.au_add(v3, 0xffffffffffffffffL);
        final long v5 = AuInt.au_or(v2, v4);
        final long v6 = AuInt.au_sraw(v1, v5);
        // the answer is int32, 32 bits
        return ((v6) & 0xffffffffL);
    }
}
