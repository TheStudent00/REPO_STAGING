// arch-unit 473  --  go  `a == b`  lhs=bool rhs=bool
// symbol main.op_491   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sub t0, a0, a1                       integer    operator:-
//   sltiu a0, t0, 0x1                    integer    operator:< unsigned
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: bool, 1 bits.  parameters are operand bit patterns.
public final class au_473_go_eq_bool_bool {

    public static long au_473_go_eq_bool_bool(long p0, long p1) {
        // a0: operand `a` (bool) zero-extended to XLEN
        final long v1 = ((p0) & 0x1L);
        // a1: operand `b` (bool) zero-extended to XLEN
        final long v2 = ((p1) & 0x1L);
        final long v3 = AuInt.au_sub(v1, v2);
        final long v4 = AuInt.au_sltu(v3, 0x1L);
        // the answer is bool, 1 bits
        return ((v4) & 0x1L);
    }
}
