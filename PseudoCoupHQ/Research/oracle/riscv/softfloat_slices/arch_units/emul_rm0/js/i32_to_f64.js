'use strict';
const { sfUdiv, sfSgn, sfCtlz, sfAbs, sfUsubsat, sfFshl } = require('./helpers.js');


function i32_to_f64_rm0(v_arg) {
  const v_i = ((v_arg === 0x0n) ? 1n : 0n);
  const v__n7 = (v_i ^ 0x1n);
  const v__m8 = (sfSgn(v__n7, 0x1n) & 0xffffffffffffffffn);
  const v__k1 = sfAbs(v_arg, 0x20n);
  const v__k2 = sfCtlz(v__k1, 0x20n);
  const v_i3 = v__k2;
  const v_i12 = (v__k1);
  const v_i4 = ((v_i3 + 0x15n) & 0xffffffffn);
  const v_i8 = ((0x41dn - v_i3) & 0xffffffffn);
  const v_i9 = (v_i8);
  const v__sh5 = ((v_i9 << (0x34n & 0x3fn)) & 0xffffffffffffffffn);
  const v_i13 = (v_i4);
  const v__sh6 = ((v_i12 << (v_i13 & 0x3fn)) & 0xffffffffffffffffn);
  const v_i14 = v__sh6;
  const v__sh3 = (v_arg >> (0x1fn & 0x1fn));
  const v_i6 = (v__sh3);
  const v__sh4 = ((v_i6 << (0x3fn & 0x3fn)) & 0xffffffffffffffffn);
  const v_i11 = (v__sh5 | v__sh4);
  const v_i15 = ((v_i11 + v_i14) & 0xffffffffffffffffn);
  const v__a9 = (v_i15 & v__m8);
  return v__a9;
}
module.exports = { i32_to_f64_rm0 };
