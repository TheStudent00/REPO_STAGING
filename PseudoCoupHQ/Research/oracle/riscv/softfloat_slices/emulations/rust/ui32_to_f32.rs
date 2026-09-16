#![allow(non_snake_case, unused_parens, unused_imports, unused_variables, unused_comparisons, clippy::all)]
use crate::helpers::*;


pub fn ui32_to_f32_rm1(v_arg: u32) -> u64 {
    let v_i: bool = (v_arg == 0x0u32);
    let v__n23: bool = (v_i ^ true);
    let v__m24: u32 = (0u32.wrapping_sub((v__n23) as u32));
    let v_i2: bool = (((v_arg) as i32) > (-1i32));
    let v__k1: u32 = sf_ctlz_u32(v_arg);
    let v_i10: u32 = v__k1;
    let v_i11: u8 = ((v_i10) as u8);
    let v_i12: u8 = v_i11.wrapping_add(0xffu8);
    let v_i13: u32 = ((v_i12) as u32);
    let v_i14: u16 = ((v_i12) as u16);
    let v_i15: u16 = 0x9cu16.wrapping_sub(v_i14);
    let v_i16: bool = (v_arg < 0x1000000u32);
    let v__sh3: u32 = v_arg.wrapping_shr((0x8u32) as u32);
    let v_i8: u32 = v__sh3.wrapping_add(0x4e800000u32);
    let v_i18: u32 = ((v_i15) as u32);
    let v__sh4: u32 = v_i18.wrapping_shl((0x17u32) as u32);
    let v_i19: u32 = v__sh4;
    let v_i20: u32 = v_i13.wrapping_add(0xfffffff9u32);
    let v__sh5: u32 = v_arg.wrapping_shl((v_i20) as u32);
    let v_i21: u32 = v__sh5;
    let v_i22: u32 = v_i21.wrapping_add(v_i19);
    let v__sh6: u32 = v_arg.wrapping_shl((v_i13) as u32);
    let v_i23: u32 = v__sh6;
    let v__sh7: u32 = v_i23.wrapping_shr((0x7u32) as u32);
    let v_i27: bool = (v_i23 < 0x80u32);
    let v__m9: u32 = (0u32.wrapping_sub((v_i27) as u32));
    let v__n10: u32 = (v__m9 ^ 0xffffffffu32);
    let v_i30: u32 = (v_i19 & v__n10);
    let v_i31: u32 = v__sh7.wrapping_add(v_i30);
    let v__n11: bool = (v_i2 ^ true);
    let v__m12: u32 = (0u32.wrapping_sub((v__n11) as u32));
    let v__a13: u32 = (v_i8 & v__m12);
    let v__m15: u32 = (0u32.wrapping_sub((v_i16) as u32));
    let v__a16: u32 = (v_i22 & v__m15);
    let v__o17: u32 = (v__a13 | v__a16);
    let v__n18: bool = (v_i16 ^ true);
    let v__c19: bool = (v__n18 & v_i2);
    let v__m20: u32 = (0u32.wrapping_sub((v__c19) as u32));
    let v__a21: u32 = (v_i31 & v__m20);
    let v__o22: u32 = (v__o17 | v__a21);
    let v__a25: u32 = (v__o22 & v__m24);
    let v_i32: u64 = ((v__a25) as u64);
    v_i32
}
