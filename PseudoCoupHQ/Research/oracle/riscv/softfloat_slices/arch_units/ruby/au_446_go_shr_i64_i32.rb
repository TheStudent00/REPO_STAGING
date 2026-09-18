# arch-unit 446  --  go  `a >> b`  lhs=int64 rhs=int32
# symbol main.op_210   outcome LIFTED   24 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   ld t1, 0x10(s11)                     prologue   stack-growth check -> elided
#   bltu t1, sp, 0x6c738 <main.op_210+0x18> prologue   stack-growth check -> elided
#   c.sdsp a0, 0x8(sp)                   prologue   frame bookkeeping -> elided
#   c.swsp a1, 0x10(sp)                  prologue   stack-growth spill -> elided
#   jal t0, 0x6a790 <runtime.morestack_noctxt.abi0> prologue   stack-growth call / restart / panic tail -> elided
#   c.ldsp a0, 0x8(sp)                   prologue   frame bookkeeping -> elided
#   c.lwsp a1, 0x10(sp)                  prologue   stack-growth reload -> elided
#   jal zero, 0x6c720 <main.op_210>      prologue   stack-growth call / restart / panic tail -> elided
#   sd ra, -0x8(sp)                      frame      frame bookkeeping -> elided
#   c.addi sp, -0x8                      frame      frame bookkeeping -> elided
#   c.sdsp ra, 0x0(sp)                   frame      frame bookkeeping -> elided
#   addiw t0, a1, 0x0                    integer    operator:+ then sign-extend the low 32 bits
#   blt t0, zero, 0x6c766 <main.op_210+0x46> guard      guard branch -> a `_trap` predicate
#   slli t0, a1, 0x20                    integer    operator:<<
#   srli t0, t0, 0x20                    integer    operator:>> unsigned
#   sltiu t0, t0, 0x40                   integer    operator:< unsigned
#   c.addi t0, -0x1                      integer    operator:+
#   or t0, a1, t0                        integer    operator:|
#   sra a0, a0, t0                       integer    arithmetic right shift, written out in unsigned bit operations
#   c.ldsp ra, 0x0(sp)                   frame      frame bookkeeping -> elided
#   c.addi sp, 0x8                       frame      frame bookkeeping -> elided
#   jalr zero, 0x0(ra)                   integer    return
#   jal ra, 0x40830 <runtime.panicshift> trap-tail  the runtime panic the guard branches to -> the `_trap` predicate
#   c.nop                                trap-tail  the runtime panic the guard branches to -> the `_trap` predicate
#
# answer: int64, 64 bits.  parameters are operand bit patterns.
#
# GUARDED: this arch-unit branches to a go runtime panic.  The function
# below is the fall-through; the companion `_trap` predicate is 1 exactly
# when the arch-unit takes the branch instead.
require_relative 'au_int'

def au_446_go_shr_i64_i32(p0, p1)
  # a0: operand `a` (int64) arrives in a0
  v1 = p0
  # a1: operand `b` (int32) sign-extended to XLEN, as the ABI presents it
  v2 = au_sext32(p1)
  v3 = au_addw(v2, 0x0)
  v4 = au_sll(v2, 0x20)
  v5 = au_srl(v4, 0x20)
  v6 = au_sltu(v5, 0x40)
  v7 = au_add(v6, 0xffffffffffffffff)
  v8 = au_or(v2, v7)
  v9 = au_sra(v1, v8)
  # the answer is int64, 64 bits
  v9
end

def au_446_go_shr_i64_i32_trap(p0, p1)
  # a0: operand `a` (int64) arrives in a0
  v1 = p0
  # a1: operand `b` (int32) sign-extended to XLEN, as the ABI presents it
  v2 = au_sext32(p1)
  v3 = au_addw(v2, 0x0)
  au_ltz(v3)
end
