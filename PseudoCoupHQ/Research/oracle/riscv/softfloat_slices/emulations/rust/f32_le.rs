#![allow(non_snake_case, unused_parens, unused_imports, unused_variables, unused_comparisons, clippy::all)]
use crate::helpers::*;


pub fn f32_le_rm1(v_arg: u64, v_arg1: u64) -> bool {
    let v_i: u32 = ((v_arg) as u32);
    let v_i2: u32 = ((v_arg1) as u32);
    let v_i3: u32 = (v_i & 0x7f800000u32);
    let v_i4: bool = (v_i3 != 0x7f800000u32);
    let v_i5: u32 = (v_i & 0x7fffffu32);
    let v_i6: bool = (v_i5 == 0x0u32);
    let v_i7: bool = (v_i4 | v_i6);
    let v_i9: u32 = (v_i2 & 0x7f800000u32);
    let v_i10: bool = (v_i9 != 0x7f800000u32);
    let v_i11: u32 = (v_i2 & 0x7fffffu32);
    let v_i12: bool = (v_i11 == 0x0u32);
    let v_i13: bool = (v_i10 | v_i12);
    let v__c5: bool = (v_i7 & v_i13);
    let v_i15: u32 = (v_i2 ^ v_i);
    let v_i16: bool = (((v_i15) as i32) > (-1i32));
    let v_i18: bool = (((v_i) as i32) < (0i32));
    let v_i19: u32 = (v_i2 & 0x7fffffffu32);
    let v_i20: u32 = (v_i19 | v_i);
    let v_i21: bool = (v_i20 == 0x0u32);
    let v_i22: bool = (v_i18 | v_i21);
    let v_i24: bool = (v_i == v_i2);
    let v_i25: bool = (v_i < v_i2);
    let v_i27: bool = (v_i18 ^ v_i25);
    let v_i28: bool = (v_i24 | v_i27);
    let v__a3: bool = (v_i28 & v_i16);
    let v__n1: bool = (v_i16 ^ true);
    let v__a2: bool = (v_i22 & v__n1);
    let v__o4: bool = (v__a2 | v__a3);
    let v__a6: bool = (v__o4 & v__c5);
    v__a6
}
