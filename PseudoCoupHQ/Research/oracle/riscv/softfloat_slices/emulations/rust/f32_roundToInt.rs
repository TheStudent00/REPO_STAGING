#![allow(non_snake_case, unused_parens, unused_imports, unused_variables, unused_comparisons, clippy::all)]
use crate::helpers::*;


pub fn f32_roundToInt_rm1(v_arg: u64, v_arg1: bool) -> u64 {
    let v_i: u32 = ((v_arg) as u32);
    let v_i2: u32 = v_i.wrapping_shr((0x17u32) as u32);
    let v_i3: u32 = (v_i2 & 0xffu32);
    let v_i4: bool = (v_i3 < 0x7fu32);
    let v_i6: u32 = (v_i & 0x7fffffffu32);
    let v_i7: bool = (v_i6 == 0x0u32);
    let v__m1: u32 = (0u32.wrapping_sub((v_i7) as u32));
    let v_i8: u32 = (v_i & 0x80000000u32);
    let v__a2: u32 = (v_i & v__m1);
    let v__n3: u32 = (v__m1 ^ 0xffffffffu32);
    let v__a4: u32 = (v_i8 & v__n3);
    let v_spec_select: u32 = (v__a2 | v__a4);
    let v_i10: bool = (v_i3 > 0x95u32);
    let v_i12: bool = (v_i3 != 0xffu32);
    let v_i17: u32 = 0x96u32.wrapping_sub(v_i3);
    let v__sh9: u32 = 0xffffffffu32.wrapping_shl((v_i17) as u32);
    let v__neg: u32 = v__sh9;
    let v_i18: u32 = (v__neg & v_i);
    let v_i13: u32 = (v_i & 0x7fffffu32);
    let v_i14: bool = (v_i13 == 0x0u32);
    let v_i15: bool = (v_i14 | v_i12);
    let v__m5: u32 = (0u32.wrapping_sub((v_i15) as u32));
    let v__a6: u32 = (v_i & v__m5);
    let v__n7: u32 = (v__m5 ^ 0xffffffffu32);
    let v__a8: u32 = (0x7fc00000u32 & v__n7);
    let v_spec_select4: u32 = (v__a6 | v__a8);
    let v__n10: bool = (v_i10 ^ true);
    let v__n11: bool = (v_i4 ^ true);
    let v__c12: bool = (v__n10 & v__n11);
    let v__m13: u32 = (0u32.wrapping_sub((v__c12) as u32));
    let v__a14: u32 = (v_i18 & v__m13);
    let v__m15: u32 = (0u32.wrapping_sub((v_i4) as u32));
    let v__a16: u32 = (v_spec_select & v__m15);
    let v__o17: u32 = (v__a14 | v__a16);
    let v__m19: u32 = (0u32.wrapping_sub((v_i10) as u32));
    let v__a20: u32 = (v_spec_select4 & v__m19);
    let v__o21: u32 = (v__o17 | v__a20);
    let v_i20: u64 = ((v__o21) as u64);
    v_i20
}
