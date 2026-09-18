// arch-unit 3  --  c  `-a`  lhs=double rhs=None
// symbol op_16   outcome WALK_REFUSED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fsgnjn.d fa0, fa0, fa0             float    bit-manipulation
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
'use strict';
const AF = require('./au_float.js');

function au_003_c_neg_f64(p0) {
  // fa0: operand `a` (double) arrives in fa0
  const v1 = p0;
  const v2 = (((v1) & 0x7fffffffffffffffn) | (((~(v1)) & 0xffffffffffffffffn) & 0x8000000000000000n));
  return v2;
}

module.exports = { au_003_c_neg_f64 };
