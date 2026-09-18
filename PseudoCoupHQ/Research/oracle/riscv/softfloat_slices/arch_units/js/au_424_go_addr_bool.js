// arch-unit 424  --  go  `&a`  lhs=bool rhs=None
// symbol main.op_35   outcome LIFTED   18 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   ld t1, 0x10(s11)                     memory     the store/load the reduction *(&a) reads
//   bltu t1, sp, 0x6c6d8 <main.op_35+0x18> integer    stack-growth check -> elided
//   sb a0, 0x8(sp)                       memory     the store/load the reduction *(&a) reads
//   jal t0, 0x6a730 <runtime.morestack_noctxt.abi0> address    a call into the go runtime
//   lbu a0, 0x8(sp)                      memory     the store/load the reduction *(&a) reads
//   jal zero, 0x6c6c0 <main.op_35>       address    a call into the go runtime
//   sd ra, -0x20(sp)                     memory     the store/load the reduction *(&a) reads
//   c.addi16sp sp, -0x20                 address    a stack address / frame adjustment -- not a bit function
//   c.sdsp ra, 0x0(sp)                   memory     the store/load the reduction *(&a) reads
//   sb a0, 0x28(sp)                      memory     the store/load the reduction *(&a) reads
//   auipc a0, 0xa                        address    the heap allocator -- not a bit function
//   addi a0, a0, -0x284                  integer    operator:+
//   jal ra, 0x23b60 <runtime.newobject>  address    the heap allocator -- not a bit function
//   lb t0, 0x28(sp)                      memory     the store/load the reduction *(&a) reads
//   sb t0, 0x0(a0)                       memory     the store/load the reduction *(&a) reads
//   c.ldsp ra, 0x0(sp)                   memory     the store/load the reduction *(&a) reads
//   c.addi16sp sp, 0x20                  address    a stack address / frame adjustment -- not a bit function
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: bool, 1 bits.  parameters are operand bit patterns.
//
// REDUCED: `&a` yields an address, which is not a function of the
// operand bits.  What is emulated and verified here is *(&a).
'use strict';
const AU = require('./au_int.js');

function au_424_go_addr_bool(p0) {
  // REDUCED: the emulated function is *(&a) -- the bit pattern the store/load moves
  return ((p0) & 0x1n);
}

module.exports = { au_424_go_addr_bool };
