'use strict';
const { sfUdiv, sfSgn, sfCtlz, sfAbs, sfUsubsat, sfFshl } = require('./helpers.js');


function ui32_to_f64_rm0(v_arg) {
  const v_i = ((v_arg === 0x0n) ? 1n : 0n);
  const v__n4 = (v_i ^ 0x1n);
  const v__m5 = (sfSgn(v__n4, 0x1n) & 0xffffffffffffffffn);
  const v__k1 = sfCtlz(v_arg, 0x20n);
  const v_i2 = v__k1;
  const v_i3 = ((v_i2 + 0x15n) & 0xffffffffn);
  const v_i4 = ((0x41dn - v_i2) & 0xffffffffn);
  const v_i5 = (v_i4);
  const v__sh2 = ((v_i5 << (0x34n & 0x3fn)) & 0xffffffffffffffffn);
  const v_i8 = (v_i3);
  const v_i7 = (v_arg);
  const v__sh3 = ((v_i7 << (v_i8 & 0x3fn)) & 0xffffffffffffffffn);
  const v_i9 = v__sh3;
  const v_i10 = ((v__sh2 + v_i9) & 0xffffffffffffffffn);
  const v__a6 = (v_i10 & v__m5);
  return v__a6;
}
module.exports = { ui32_to_f64_rm0 };
