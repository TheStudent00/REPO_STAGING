#![allow(non_snake_case, unused_parens, unused_imports, unused_variables, unused_comparisons, clippy::all)]
use crate::helpers::*;


pub fn f32_roundToInt_rm0(v_arg: u64, v_arg1: bool) -> u64 {
    let v_i: u32 = ((v_arg) as u32);
    let v_i2: u32 = v_i.wrapping_shr((0x17u32) as u32);
    let v_i3: u32 = (v_i2 & 0xffu32);
    let v_i4: bool = (v_i3 < 0x7fu32);
    let v_i16: bool = (v_i3 > 0x95u32);
    let v_i6: u32 = (v_i & 0x7fffffffu32);
    let v_i7: bool = (v_i6 == 0x0u32);
    let v_i18: bool = (v_i3 != 0xffu32);
    let v_i19: u32 = (v_i & 0x7fffffu32);
    let v_i20: bool = (v_i19 == 0x0u32);
    let v_i21: bool = (v_i20 | v_i18);
    let v__m1: u32 = (0u32.wrapping_sub((v_i21) as u32));
    let v__a2: u32 = (v_i & v__m1);
    let v__n3: u32 = (v__m1 ^ 0xffffffffu32);
    let v__a4: u32 = (0x7fc00000u32 & v__n3);
    let v_spec_select4: u32 = (v__a2 | v__a4);
    let v_i23: u32 = 0x96u32.wrapping_sub(v_i3);
    let v__sh5: u32 = 0x1u32.wrapping_shl((v_i23) as u32);
    let v_i24: u32 = v__sh5;
    let v_i12: bool = (v_i3 == 0x7eu32);
    let v_i25: u32 = v_i24.wrapping_add(0xffffffffu32);
    let v__sh6: u32 = v_i24.wrapping_shr((0x1u32) as u32);
    let v_i27: u32 = v__sh6.wrapping_add(v_i);
    let v_i28: u32 = (v_i27 & v_i25);
    let v_i29: bool = (v_i28 == 0x0u32);
    let v__m7: u32 = (0u32.wrapping_sub((v_i29) as u32));
    let v_i30: u32 = (v_i24 ^ 0xffffffffu32);
    let v__a8: u32 = (v_i30 & v__m7);
    let v__n9: u32 = (v__m7 ^ 0xffffffffu32);
    let v_i31: u32 = (v__a8 | v__n9);
    let v_i32: u32 = 0x0u32.wrapping_sub(v_i24);
    let v_i33: u32 = (v_i31 & v_i32);
    let v_i34: u32 = (v_i33 & v_i27);
    let v_i9: u32 = (v_i & 0x80000000u32);
    let v_i11: bool = (v_i19 != 0x0u32);
    let v_i13: bool = (v_i11 & v_i12);
    let v__m11: u32 = (0u32.wrapping_sub((v_i13) as u32));
    let v_i14: u32 = (v_i9 | 0x3f800000u32);
    let v__a12: u32 = (v_i14 & v__m11);
    let v__n13: u32 = (v__m11 ^ 0xffffffffu32);
    let v__a14: u32 = (v_i9 & v__n13);
    let v_spec_select: u32 = (v__a12 | v__a14);
    let v__c15: bool = (v_i7 & v_i4);
    let v__m16: u32 = (0u32.wrapping_sub((v__c15) as u32));
    let v__a17: u32 = (v_i & v__m16);
    let v__n18: bool = (v_i7 ^ true);
    let v__c19: bool = (v__n18 & v_i4);
    let v__m20: u32 = (0u32.wrapping_sub((v__c19) as u32));
    let v__a21: u32 = (v_spec_select & v__m20);
    let v__o22: u32 = (v__a17 | v__a21);
    let v__n24: bool = (v_i4 ^ true);
    let v__n23: bool = (v_i16 ^ true);
    let v__c25: bool = (v__n23 & v__n24);
    let v__m26: u32 = (0u32.wrapping_sub((v__c25) as u32));
    let v__a27: u32 = (v_i34 & v__m26);
    let v__o28: u32 = (v__o22 | v__a27);
    let v__m30: u32 = (0u32.wrapping_sub((v_i16) as u32));
    let v__a31: u32 = (v_spec_select4 & v__m30);
    let v__o32: u32 = (v__o28 | v__a31);
    let v_i36: u64 = ((v__o32) as u64);
    v_i36
}
