'use strict';
const { sfUdiv, sfSgn, sfCtlz, sfAbs, sfUsubsat, sfFshl } = require('./helpers.js');


function f16_le_quiet_rm1(v_arg, v_arg1) {
  const v_i = (v_arg & 0xffffffffn);
  const v_i2 = (v_i & 0xffffn);
  const v_i3 = (v_arg1 & 0xffffffffn);
  const v_i4 = (v_i3 & 0xffffn);
  const v_i5 = (v_i & 0x7c00n);
  const v_i6 = ((v_i5 !== 0x7c00n) ? 1n : 0n);
  const v_i7 = (v_i & 0x3ffn);
  const v_i8 = ((v_i7 === 0x0n) ? 1n : 0n);
  const v_i9 = (v_i6 | v_i8);
  const v_i21 = (v_i3 | v_i);
  const v_i22 = (v_i21 & 0x7fffn);
  const v_i23 = ((v_i22 === 0x0n) ? 1n : 0n);
  const v_i11 = (v_i3 & 0x7c00n);
  const v_i12 = ((v_i11 !== 0x7c00n) ? 1n : 0n);
  const v_i13 = (v_i3 & 0x3ffn);
  const v_i14 = ((v_i13 === 0x0n) ? 1n : 0n);
  const v_i15 = (v_i12 | v_i14);
  const v__c5 = (v_i9 & v_i15);
  const v_i17 = ((v_i2 > 0x7fffn) ? 1n : 0n);
  const v_i24 = (v_i17 | v_i23);
  const v_i18 = ((v_i4 < 0x8000n) ? 1n : 0n);
  const v_i19 = (v_i17 ^ v_i18);
  const v_i26 = ((v_i2 === v_i4) ? 1n : 0n);
  const v_i27 = ((v_i2 < v_i4) ? 1n : 0n);
  const v_i28 = (v_i17 ^ v_i27);
  const v_i29 = (v_i26 | v_i28);
  const v__a3 = (v_i29 & v_i19);
  const v__n1 = (v_i19 ^ 0x1n);
  const v__a2 = (v_i24 & v__n1);
  const v__o4 = (v__a2 | v__a3);
  const v__a6 = (v__o4 & v__c5);
  return v__a6;
}
module.exports = { f16_le_quiet_rm1 };
