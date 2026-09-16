#![allow(non_snake_case, unused_parens, unused_imports, unused_variables, unused_comparisons, clippy::all)]
use crate::helpers::*;


pub fn f16_le_quiet_rm1(v_arg: u64, v_arg1: u64) -> bool {
    let v_i: u32 = ((v_arg) as u32);
    let v_i2: u32 = (v_i & 0xffffu32);
    let v_i3: u32 = ((v_arg1) as u32);
    let v_i4: u32 = (v_i3 & 0xffffu32);
    let v_i5: u32 = (v_i & 0x7c00u32);
    let v_i6: bool = (v_i5 != 0x7c00u32);
    let v_i7: u32 = (v_i & 0x3ffu32);
    let v_i8: bool = (v_i7 == 0x0u32);
    let v_i9: bool = (v_i6 | v_i8);
    let v_i21: u32 = (v_i3 | v_i);
    let v_i22: u32 = (v_i21 & 0x7fffu32);
    let v_i23: bool = (v_i22 == 0x0u32);
    let v_i11: u32 = (v_i3 & 0x7c00u32);
    let v_i12: bool = (v_i11 != 0x7c00u32);
    let v_i13: u32 = (v_i3 & 0x3ffu32);
    let v_i14: bool = (v_i13 == 0x0u32);
    let v_i15: bool = (v_i12 | v_i14);
    let v__c5: bool = (v_i9 & v_i15);
    let v_i17: bool = (v_i2 > 0x7fffu32);
    let v_i24: bool = (v_i17 | v_i23);
    let v_i18: bool = (v_i4 < 0x8000u32);
    let v_i19: bool = (v_i17 ^ v_i18);
    let v_i26: bool = (v_i2 == v_i4);
    let v_i27: bool = (v_i2 < v_i4);
    let v_i28: bool = (v_i17 ^ v_i27);
    let v_i29: bool = (v_i26 | v_i28);
    let v__a3: bool = (v_i29 & v_i19);
    let v__n1: bool = (v_i19 ^ true);
    let v__a2: bool = (v_i24 & v__n1);
    let v__o4: bool = (v__a2 | v__a3);
    let v__a6: bool = (v__o4 & v__c5);
    v__a6
}
