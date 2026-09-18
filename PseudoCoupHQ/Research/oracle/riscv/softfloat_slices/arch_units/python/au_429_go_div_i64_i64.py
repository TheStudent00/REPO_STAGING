# arch-unit 429  --  go  `a / b`  lhs=int64 rhs=int64
# symbol main.op_103   outcome LIFTED   18 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   ld t1, 0x10(s11)                     prologue   stack-growth check -> elided
#   bltu t1, sp, 0x6c738 <main.op_103+0x18> prologue   stack-growth check -> elided
#   c.sdsp a0, 0x8(sp)                   prologue   frame bookkeeping -> elided
#   c.sdsp a1, 0x10(sp)                  prologue   frame bookkeeping -> elided
#   jal t0, 0x6a790 <runtime.morestack_noctxt.abi0> prologue   stack-growth call / restart / panic tail -> elided
#   c.ldsp a0, 0x8(sp)                   prologue   frame bookkeeping -> elided
#   c.ldsp a1, 0x10(sp)                  prologue   frame bookkeeping -> elided
#   jal zero, 0x6c720 <main.op_103>      prologue   stack-growth call / restart / panic tail -> elided
#   sd ra, -0x8(sp)                      frame      frame bookkeeping -> elided
#   c.addi sp, -0x8                      frame      frame bookkeeping -> elided
#   c.sdsp ra, 0x0(sp)                   frame      frame bookkeeping -> elided
#   beq a1, zero, 0x6c750 <main.op_103+0x30> guard      guard branch -> a `_trap` predicate
#   div a0, a0, a1                       integer    written-out restoring division (NOT the language's /)
#   c.ldsp ra, 0x0(sp)                   frame      frame bookkeeping -> elided
#   c.addi sp, 0x8                       frame      frame bookkeeping -> elided
#   jalr zero, 0x0(ra)                   integer    return
#   jal ra, 0x40878 <runtime.panicdivide> trap-tail  the runtime panic the guard branches to -> the `_trap` predicate
#   c.nop                                trap-tail  the runtime panic the guard branches to -> the `_trap` predicate
#
# answer: int64, 64 bits.  parameters are operand bit patterns.
#
# GUARDED: this arch-unit branches to a go runtime panic.  The function
# below is the fall-through; the companion `_trap` predicate is 1 exactly
# when the arch-unit takes the branch instead.
from au_int import *        # noqa: F401,F403

def au_429_go_div_i64_i64(p0, p1):
    # a0: operand `a` (int64) arrives in a0
    v1 = p0
    # a1: operand `b` (int64) arrives in a1
    v2 = p1
    v3 = au_div(v1, v2)
    # the answer is int64, 64 bits
    return v3

def au_429_go_div_i64_i64_trap(p0, p1):
    # a0: operand `a` (int64) arrives in a0
    v1 = p0
    # a1: operand `b` (int64) arrives in a1
    v2 = p1
    return au_eqz(v2)
