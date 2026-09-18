'use strict';
const { sfUdiv, sfSgn, sfCtlz, sfAbs, sfUsubsat, sfFshl } = require('./helpers.js');


function f64_lt_quiet_rm1(v_arg, v_arg1) {
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
  const v__c5 = (v_i5 & v_i11);
  const v_i13 = (v_arg1 ^ v_arg);
  const v_i14 = ((sfSgn(v_i13, 0x40n) > (-1n)) ? 1n : 0n);
  const v_i16 = ((sfSgn(v_arg, 0x40n) < (0n)) ? 1n : 0n);
  const v_i17 = (v_arg1 | v_arg);
  const v_i18 = (v_i17 & 0x7fffffffffffffffn);
  const v_i19 = ((v_i18 !== 0x0n) ? 1n : 0n);
  const v_i20 = (v_i16 & v_i19);
  const v_i22 = ((v_arg !== v_arg1) ? 1n : 0n);
  const v_i23 = ((v_arg < v_arg1) ? 1n : 0n);
  const v_i25 = (v_i16 ^ v_i23);
  const v_i26 = (v_i22 & v_i25);
  const v__a3 = (v_i26 & v_i14);
  const v__n1 = (v_i14 ^ 0x1n);
  const v__a2 = (v_i20 & v__n1);
  const v__o4 = (v__a2 | v__a3);
  const v__a6 = (v__o4 & v__c5);
  return v__a6;
}
module.exports = { f64_lt_quiet_rm1 };
