'use strict';
const { sfUdiv, sfSgn, sfCtlz, sfAbs, sfUsubsat, sfFshl } = require('./helpers.js');


function f16_roundToInt_rm1(v_arg, v_arg1) {
  const v_i = (v_arg & 0xffffn);
  const v_i2 = (v_arg & 0xffffffffn);
  const v_i3 = (v_i2 >> (0xan & 0x1fn));
  const v_i4 = (v_i3 & 0x1fn);
  const v_i14 = (v_i2 & 0x3ffn);
  const v_i15 = ((v_i14 === 0x0n) ? 1n : 0n);
  const v_i5 = ((v_i4 < 0xfn) ? 1n : 0n);
  const v_i11 = ((v_i4 > 0x18n) ? 1n : 0n);
  const v_i7 = (v_arg & 0x7fffn);
  const v_i8 = ((v_i7 === 0x0n) ? 1n : 0n);
  const v__m1 = (sfSgn(v_i8, 0x1n) & 0xffffn);
  const v_i9 = (v_i & 0x8000n);
  const v__a2 = (v_i & v__m1);
  const v__n3 = (v__m1 ^ 0xffffn);
  const v__a4 = (v_i9 & v__n3);
  const v_spec_select = (v__a2 | v__a4);
  const v_i13 = ((v_i4 !== 0x1fn) ? 1n : 0n);
  const v_i16 = (v_i15 | v_i13);
  const v__m5 = (sfSgn(v_i16, 0x1n) & 0xffffn);
  const v_i18 = ((0x19n - v_i4) & 0xffffffffn);
  const v__sh9 = ((0xffffn << (v_i18 & 0x1fn)) & 0xffffffffn);
  const v_i19 = v__sh9;
  const v_i20 = (v_i19 & 0xffffn);
  const v_i21 = (v_i & v_i20);
  const v__a6 = (v_i & v__m5);
  const v__n7 = (v__m5 ^ 0xffffn);
  const v__a8 = (0x7e00n & v__n7);
  const v_spec_select4 = (v__a6 | v__a8);
  const v__n10 = (v_i11 ^ 0x1n);
  const v__n11 = (v_i5 ^ 0x1n);
  const v__c12 = (v__n10 & v__n11);
  const v__m13 = (sfSgn(v__c12, 0x1n) & 0xffffn);
  const v__a14 = (v_i21 & v__m13);
  const v__m15 = (sfSgn(v_i5, 0x1n) & 0xffffn);
  const v__a16 = (v_spec_select & v__m15);
  const v__o17 = (v__a14 | v__a16);
  const v__m19 = (sfSgn(v_i11, 0x1n) & 0xffffn);
  const v__a20 = (v_spec_select4 & v__m19);
  const v__o21 = (v__o17 | v__a20);
  const v_i23 = (v__o21);
  return v_i23;
}
module.exports = { f16_roundToInt_rm1 };
