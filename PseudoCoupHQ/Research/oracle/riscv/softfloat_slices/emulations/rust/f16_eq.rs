#![allow(non_snake_case, unused_parens, unused_imports, unused_variables, unused_comparisons, clippy::all)]
use crate::helpers::*;


pub fn f16_eq_rm1(v_arg: u64, v_arg1: u64) -> bool {
    let v_i: u32 = ((v_arg) as u32);
    let v_i2: u32 = ((v_arg1) as u32);
    let v_i3: u32 = (v_i & 0x7c00u32);
    let v_i4: bool = (v_i3 != 0x7c00u32);
    let v_i5: u32 = (v_i & 0x3ffu32);
    let v_i6: bool = (v_i5 == 0x0u32);
    let v_i7: bool = (v_i4 | v_i6);
    let v_i9: u32 = (v_i2 & 0x7c00u32);
    let v_i10: bool = (v_i9 != 0x7c00u32);
    let v_i11: u32 = (v_i2 & 0x3ffu32);
    let v_i12: bool = (v_i11 == 0x0u32);
    let v_i13: bool = (v_i10 | v_i12);
    let v__c1: bool = (v_i7 & v_i13);
    let v_i15: u32 = (v_i2 ^ v_i);
    let v_i18: u32 = (v_i2 | v_i);
    let v_i16: u32 = (v_i15 & 0xffffu32);
    let v_i17: bool = (v_i16 == 0x0u32);
    let v_i19: u32 = (v_i18 & 0x7fffu32);
    let v_i20: bool = (v_i19 == 0x0u32);
    let v_i21: bool = (v_i17 | v_i20);
    let v__a2: bool = (v_i21 & v__c1);
    v__a2
}
