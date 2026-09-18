# arch-unit 153  --  go  `&a`  lhs=float64 rhs=None
# symbol main.op_34   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   ld t1, 0x10(s11)                   integer  address/stack/runtime -- not a bit function
#   bltu t1, sp, 0x6c6d4 <main.op_34+0x14> integer  address/stack/runtime -- not a bit function
#   c.fsdsp fa0, 0x8(sp)               float    bit-manipulation
#   jal t0, 0x6a730 <runtime.morestack_noctxt.abi0> integer  address/stack/runtime -- not a bit function
#   c.fldsp fa0, 0x8(sp)               float    bit-manipulation
#   jal zero, 0x6c6c0 <main.op_34>     integer  address/stack/runtime -- not a bit function
#   sd ra, -0x20(sp)                   integer  address/stack/runtime -- not a bit function
#   c.addi16sp sp, -0x20               integer  address/stack/runtime -- not a bit function
#   c.sdsp ra, 0x0(sp)                 integer  address/stack/runtime -- not a bit function
#   c.fsdsp fa0, 0x28(sp)              float    bit-manipulation
#   auipc a0, 0xa                      integer  address/stack/runtime -- not a bit function
#   addi a0, a0, -0x2be                integer  address/stack/runtime -- not a bit function
#   jal ra, 0x23b60 <runtime.newobject> integer  address/stack/runtime -- not a bit function
#   c.ldsp t0, 0x28(sp)                integer  address/stack/runtime -- not a bit function
#   sd t0, 0x0(a0)                     integer  address/stack/runtime -- not a bit function
#   c.ldsp ra, 0x0(sp)                 integer  address/stack/runtime -- not a bit function
#   c.addi16sp sp, 0x20                integer  address/stack/runtime -- not a bit function
#   jalr zero, 0x0(ra)                 integer  return
#
# answer: f64, 64 bits.  parameters are operand bit patterns.
#
# REDUCED: `&a` yields an address, which is not a function of the
# operand bits.  What is emulated and verified here is *(&a): the
# bit pattern the float store/load arch-opcode moves.
require_relative 'au_float'

def au_153_go_addr_f64(p0)
  p0
end
