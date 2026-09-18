'use strict';
const { sfUdiv, sfSgn, sfCtlz, sfAbs, sfUsubsat, sfFshl } = require('./helpers.js');


function f64_eq_rm0(v_arg, v_arg1) {
  const v_i = (v_arg & 0x7ff0000000000000n);
  const v_i2 = ((v_i !== 0x7ff0000000000000n) ? 1n : 0n);
  const v_i3 = (v_arg & 0xfffffffffffffn);
  const v_i4 = ((v_i3 === 0x0n) ? 1n : 0n);
  const v_i5 = (v_i2 | v_i4);
  const v_i7 = (v_arg1 & 0x7ff0000000000000n);
  const v_i8 = ((v_i7 !== 0x7ff0000000000000n) ? 1n : 0n);
  const v_i9 = (v_arg1 & 0xfffffffffffffn);
  const v_i10 = ((v_i9 === 0x0n) ? 1n : 0n);
  const v_i11 = (v_i8 | v_i10);
  const v__c1 = (v_i5 & v_i11);
  const v_i13 = ((v_arg === v_arg1) ? 1n : 0n);
  const v_i14 = (v_arg1 | v_arg);
  const v_i15 = (v_i14 & 0x7fffffffffffffffn);
  const v_i16 = ((v_i15 === 0x0n) ? 1n : 0n);
  const v_i17 = (v_i13 | v_i16);
  const v__a2 = (v_i17 & v__c1);
  return v__a2;
}
module.exports = { f64_eq_rm0 };
