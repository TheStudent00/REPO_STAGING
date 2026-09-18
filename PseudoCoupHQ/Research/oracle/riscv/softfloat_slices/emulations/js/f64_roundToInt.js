'use strict';
const { sfUdiv, sfSgn, sfCtlz, sfAbs, sfUsubsat, sfFshl } = require('./helpers.js');


function f64_roundToInt_rm1(v_arg, v_arg1) {
  const v_i = (v_arg >> (0x34n & 0x3fn));
  const v_i2 = (v_i & 0xffffffffn);
  const v_i3 = (v_i2 & 0x7ffn);
  const v_i4 = ((v_i3 < 0x3ffn) ? 1n : 0n);
  const v_i6 = (v_arg & 0x7fffffffffffffffn);
  const v_i7 = ((v_i6 === 0x0n) ? 1n : 0n);
  const v__m1 = (sfSgn(v_i7, 0x1n) & 0xffffffffffffffffn);
  const v_i8 = (v_arg & 0x8000000000000000n);
  const v__a2 = (v_arg & v__m1);
  const v__n3 = (v__m1 ^ 0xffffffffffffffffn);
  const v__a4 = (v_i8 & v__n3);
  const v_spec_select = (v__a2 | v__a4);
  const v_i10 = ((v_i3 > 0x432n) ? 1n : 0n);
  const v_i12 = ((v_i3 !== 0x7ffn) ? 1n : 0n);
  const v_i17 = ((0x433n - v_i3) & 0xffffffffn);
  const v_i18 = (v_i17);
  const v__sh9 = ((0xffffffffffffffffn << (v_i18 & 0x3fn)) & 0xffffffffffffffffn);
  const v__neg = v__sh9;
  const v_i19 = (v_arg & v__neg);
  const v_i13 = (v_arg & 0xfffffffffffffn);
  const v_i14 = ((v_i13 === 0x0n) ? 1n : 0n);
  const v_i15 = (v_i14 | v_i12);
  const v__m5 = (sfSgn(v_i15, 0x1n) & 0xffffffffffffffffn);
  const v__a6 = (v_arg & v__m5);
  const v__n7 = (v__m5 ^ 0xffffffffffffffffn);
  const v__a8 = (0x7ff8000000000000n & v__n7);
  const v_spec_select4 = (v__a6 | v__a8);
  const v__n10 = (v_i10 ^ 0x1n);
  const v__n11 = (v_i4 ^ 0x1n);
  const v__c12 = (v__n10 & v__n11);
  const v__m13 = (sfSgn(v__c12, 0x1n) & 0xffffffffffffffffn);
  const v__a14 = (v_i19 & v__m13);
  const v__m15 = (sfSgn(v_i4, 0x1n) & 0xffffffffffffffffn);
  const v__a16 = (v_spec_select & v__m15);
  const v__o17 = (v__a14 | v__a16);
  const v__m19 = (sfSgn(v_i10, 0x1n) & 0xffffffffffffffffn);
  const v__a20 = (v_spec_select4 & v__m19);
  const v__o21 = (v__o17 | v__a20);
  return v__o21;
}
module.exports = { f64_roundToInt_rm1 };
