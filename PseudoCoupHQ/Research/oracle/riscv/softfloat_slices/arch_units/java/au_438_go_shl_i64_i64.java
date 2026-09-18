// arch-unit 438  --  go  `a << b`  lhs=int64 rhs=int64
// symbol main.op_175   outcome LIFTED   21 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   ld t1, 0x10(s11)                     prologue   stack-growth check -> elided
//   bltu t1, sp, 0x6c738 <main.op_175+0x18> prologue   stack-growth check -> elided
//   c.sdsp a0, 0x8(sp)                   prologue   frame bookkeeping -> elided
//   c.sdsp a1, 0x10(sp)                  prologue   frame bookkeeping -> elided
//   jal t0, 0x6a790 <runtime.morestack_noctxt.abi0> prologue   stack-growth call / restart / panic tail -> elided
//   c.ldsp a0, 0x8(sp)                   prologue   frame bookkeeping -> elided
//   c.ldsp a1, 0x10(sp)                  prologue   frame bookkeeping -> elided
//   jal zero, 0x6c720 <main.op_175>      prologue   stack-growth call / restart / panic tail -> elided
//   sd ra, -0x8(sp)                      frame      frame bookkeeping -> elided
//   c.addi sp, -0x8                      frame      frame bookkeeping -> elided
//   c.sdsp ra, 0x0(sp)                   frame      frame bookkeeping -> elided
//   blt a1, zero, 0x6c75c <main.op_175+0x3c> guard      guard branch -> a `_trap` predicate
//   sll t0, a0, a1                       integer    operator:<< (count masked to 6 bits)
//   sltiu t1, a1, 0x40                   integer    operator:< unsigned
//   sub t1, zero, t1                     integer    operator:-
//   and a0, t0, t1                       integer    operator:&
//   c.ldsp ra, 0x0(sp)                   frame      frame bookkeeping -> elided
//   c.addi sp, 0x8                       frame      frame bookkeeping -> elided
//   jalr zero, 0x0(ra)                   integer    return
//   jal ra, 0x40830 <runtime.panicshift> trap-tail  the runtime panic the guard branches to -> the `_trap` predicate
//   c.nop                                trap-tail  the runtime panic the guard branches to -> the `_trap` predicate
//
// answer: int64, 64 bits.  parameters are operand bit patterns.
//
// GUARDED: this arch-unit branches to a go runtime panic.  The function
// below is the fall-through; the companion `_trap` predicate is 1 exactly
// when the arch-unit takes the branch instead.
public final class au_438_go_shl_i64_i64 {

    public static long au_438_go_shl_i64_i64(long p0, long p1) {
        // a0: operand `a` (int64) arrives in a0
        final long v1 = p0;
        // a1: operand `b` (int64) arrives in a1
        final long v2 = p1;
        final long v3 = AuInt.au_sll(v1, v2);
        final long v4 = AuInt.au_sltu(v2, 0x40L);
        final long v5 = AuInt.au_sub(0x0L, v4);
        final long v6 = AuInt.au_and(v3, v5);
        // the answer is int64, 64 bits
        return v6;
    }

    public static long au_438_go_shl_i64_i64_trap(long p0, long p1) {
        // a0: operand `a` (int64) arrives in a0
        final long v1 = p0;
        // a1: operand `b` (int64) arrives in a1
        final long v2 = p1;
        return AuInt.au_ltz(v2);
    }
}
