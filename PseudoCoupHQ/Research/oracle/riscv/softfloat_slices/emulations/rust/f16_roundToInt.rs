#![allow(non_snake_case, unused_parens, unused_imports, unused_variables, unused_comparisons, clippy::all)]
use crate::helpers::*;


pub fn f16_roundToInt_rm1(v_arg: u64, v_arg1: bool) -> u64 {
    let v_i: u16 = ((v_arg) as u16);
    let v_i2: u32 = ((v_arg) as u32);
    let v_i3: u32 = v_i2.wrapping_shr((0xau32) as u32);
    let v_i4: u32 = (v_i3 & 0x1fu32);
    let v_i14: u32 = (v_i2 & 0x3ffu32);
    let v_i15: bool = (v_i14 == 0x0u32);
    let v_i5: bool = (v_i4 < 0xfu32);
    let v_i11: bool = (v_i4 > 0x18u32);
    let v_i7: u64 = (v_arg & 0x7fffu64);
    let v_i8: bool = (v_i7 == 0x0u64);
    let v__m1: u16 = (0u16.wrapping_sub((v_i8) as u16));
    let v_i9: u16 = (v_i & 0x8000u16);
    let v__a2: u16 = (v_i & v__m1);
    let v__n3: u16 = (v__m1 ^ 0xffffu16);
    let v__a4: u16 = (v_i9 & v__n3);
    let v_spec_select: u16 = (v__a2 | v__a4);
    let v_i13: bool = (v_i4 != 0x1fu32);
    let v_i16: bool = (v_i15 | v_i13);
    let v__m5: u16 = (0u16.wrapping_sub((v_i16) as u16));
    let v_i18: u32 = 0x19u32.wrapping_sub(v_i4);
    let v__sh9: u32 = 0xffffu32.wrapping_shl((v_i18) as u32);
    let v_i19: u32 = v__sh9;
    let v_i20: u16 = ((v_i19) as u16);
    let v_i21: u16 = (v_i & v_i20);
    let v__a6: u16 = (v_i & v__m5);
    let v__n7: u16 = (v__m5 ^ 0xffffu16);
    let v__a8: u16 = (0x7e00u16 & v__n7);
    let v_spec_select4: u16 = (v__a6 | v__a8);
    let v__n10: bool = (v_i11 ^ true);
    let v__n11: bool = (v_i5 ^ true);
    let v__c12: bool = (v__n10 & v__n11);
    let v__m13: u16 = (0u16.wrapping_sub((v__c12) as u16));
    let v__a14: u16 = (v_i21 & v__m13);
    let v__m15: u16 = (0u16.wrapping_sub((v_i5) as u16));
    let v__a16: u16 = (v_spec_select & v__m15);
    let v__o17: u16 = (v__a14 | v__a16);
    let v__m19: u16 = (0u16.wrapping_sub((v_i11) as u16));
    let v__a20: u16 = (v_spec_select4 & v__m19);
    let v__o21: u16 = (v__o17 | v__a20);
    let v_i23: u64 = ((v__o21) as u64);
    v_i23
}
