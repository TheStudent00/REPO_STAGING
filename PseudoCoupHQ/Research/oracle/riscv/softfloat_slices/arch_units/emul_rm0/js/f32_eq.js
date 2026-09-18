'use strict';
const { sfUdiv, sfSgn, sfCtlz, sfAbs, sfUsubsat, sfFshl } = require('./helpers.js');


function f32_eq_rm0(v_arg, v_arg1) {
  const v_i = (v_arg & 0xffffffffn);
  const v_i2 = (v_arg1 & 0xffffffffn);
  const v_i3 = (v_i & 0x7f800000n);
  const v_i4 = ((v_i3 !== 0x7f800000n) ? 1n : 0n);
  const v_i5 = (v_i & 0x7fffffn);
  const v_i6 = ((v_i5 === 0x0n) ? 1n : 0n);
  const v_i7 = (v_i4 | v_i6);
  const v_i9 = (v_i2 & 0x7f800000n);
  const v_i10 = ((v_i9 !== 0x7f800000n) ? 1n : 0n);
  const v_i11 = (v_i2 & 0x7fffffn);
  const v_i12 = ((v_i11 === 0x0n) ? 1n : 0n);
  const v_i13 = (v_i10 | v_i12);
  const v__c1 = (v_i7 & v_i13);
  const v_i15 = ((v_i === v_i2) ? 1n : 0n);
  const v_i16 = (v_i2 | v_i);
  const v_i17 = (v_i16 & 0x7fffffffn);
  const v_i18 = ((v_i17 === 0x0n) ? 1n : 0n);
  const v_i19 = (v_i15 | v_i18);
  const v__a2 = (v_i19 & v__c1);
  return v__a2;
}
module.exports = { f32_eq_rm0 };
