# arch-unit 444  --  go  `a >> b`  lhs=int32 rhs=int64
# symbol main.op_205   outcome LIFTED   21 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   ld t1, 0x10(s11)                     prologue   stack-growth check -> elided
#   bltu t1, sp, 0x6c748 <main.op_205+0x18> prologue   stack-growth check -> elided
#   c.swsp a0, 0x8(sp)                   prologue   stack-growth spill -> elided
#   c.sdsp a1, 0x10(sp)                  prologue   frame bookkeeping -> elided
#   jal t0, 0x6a7a0 <runtime.morestack_noctxt.abi0> prologue   stack-growth call / restart / panic tail -> elided
#   c.lwsp a0, 0x8(sp)                   prologue   stack-growth reload -> elided
#   c.ldsp a1, 0x10(sp)                  prologue   frame bookkeeping -> elided
#   jal zero, 0x6c730 <main.op_205>      prologue   stack-growth call / restart / panic tail -> elided
#   sd ra, -0x8(sp)                      frame      frame bookkeeping -> elided
#   c.addi sp, -0x8                      frame      frame bookkeeping -> elided
#   c.sdsp ra, 0x0(sp)                   frame      frame bookkeeping -> elided
#   blt a1, zero, 0x6c76a <main.op_205+0x3a> guard      guard branch -> a `_trap` predicate
#   sltiu t0, a1, 0x20                   integer    operator:< unsigned
#   c.addi t0, -0x1                      integer    operator:+
#   or t0, a1, t0                        integer    operator:|
#   sraw a0, a0, t0                      integer    arithmetic right shift of the low 32 bits, written out
#   c.ldsp ra, 0x0(sp)                   frame      frame bookkeeping -> elided
#   c.addi sp, 0x8                       frame      frame bookkeeping -> elided
#   jalr zero, 0x0(ra)                   integer    return
#   jal ra, 0x408a0 <runtime.panicshift> trap-tail  the runtime panic the guard branches to -> the `_trap` predicate
#   c.nop                                trap-tail  the runtime panic the guard branches to -> the `_trap` predicate
#
# answer: int32, 32 bits.  parameters are operand bit patterns.
#
# GUARDED: this arch-unit branches to a go runtime panic.  The function
# below is the fall-through; the companion `_trap` predicate is 1 exactly
# when the arch-unit takes the branch instead.
from au_int import *        # noqa: F401,F403

def au_444_go_shr_i32_i64(p0, p1):
    # a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
    v1 = au_sext32(p0)
    # a1: operand `b` (int64) arrives in a1
    v2 = p1
    v3 = au_sltu(v2, 0x20)
    v4 = au_add(v3, 0xffffffffffffffff)
    v5 = au_or(v2, v4)
    v6 = au_sraw(v1, v5)
    # the answer is int32, 32 bits
    return ((v6) & 0xffffffff)

def au_444_go_shr_i32_i64_trap(p0, p1):
    # a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
    v1 = au_sext32(p0)
    # a1: operand `b` (int64) arrives in a1
    v2 = p1
    return au_ltz(v2)
