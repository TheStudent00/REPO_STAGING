// arch-unit 127  --  c  `a && b`  lhs=double rhs=bool
// symbol op_347   outcome WALK_REFUSED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fmv.d.x fa5, zero                  float    bit-manipulation
//   feq.d a1, fa0, fa5                 float    emulation:f64_eq_rm0
//   andn a0, a0, a1                    integer  operator:& ~
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
'use strict';
const AF = require('./au_float.js');

function au_127_c_land_f64_bool(p0, p1) {
  // fa0: operand `a` (double) arrives in fa0
  const v1 = p0;
  // a0: operand `b` (bool) zero-extended
  const v2 = ((p1) & 0x1n);
  const v3 = 0x0n;
  const v4 = AF.f64_eq_rm0(v1, v3);
  const v5 = ((v2) & ((~(v4)) & 0xffffffffffffffffn));
  return v5;
}

module.exports = { au_127_c_land_f64_bool };
