#![allow(non_snake_case, unused_parens, unused_imports, unused_variables, unused_comparisons, clippy::all)]
use crate::helpers::*;


pub fn ui64_to_f64_rm1(v_arg: u64) -> u64 {
    let v_i: bool = (v_arg == 0x0u64);
    let v__n23: bool = (v_i ^ true);
    let v__m24: u64 = (0u64.wrapping_sub((v__n23) as u64));
    let v_i2: bool = (((v_arg) as i64) > (-1i64));
    let v__k1: u64 = sf_ctlz_u64(v_arg);
    let v_i10: u64 = v__k1;
    let v_i11: u8 = ((v_i10) as u8);
    let v_i12: u8 = v_i11.wrapping_add(0xffu8);
    let v_i19: u64 = v_i10.wrapping_add(0xfffffff5u64);
    let v_i20: u64 = (v_i19 & 0xffffffffu64);
    let v__sh5: u64 = v_arg.wrapping_shl((v_i20) as u32);
    let v_i21: u64 = v__sh5;
    let v_i13: u16 = ((v_i12) as u16);
    let v_i14: u16 = 0x43cu16.wrapping_sub(v_i13);
    let v_i23: u64 = ((v_i12) as u64);
    let v__sh6: u64 = v_arg.wrapping_shl((v_i23) as u32);
    let v_i24: u64 = v__sh6;
    let v_i15: bool = (v_arg < 0x20000000000000u64);
    let v__sh3: u64 = v_arg.wrapping_shr((0xbu64) as u32);
    let v_i8: u64 = v__sh3.wrapping_add(0x43d0000000000000u64);
    let v_i17: u64 = ((v_i14) as u64);
    let v__sh4: u64 = v_i17.wrapping_shl((0x34u64) as u32);
    let v_i18: u64 = v__sh4;
    let v_i22: u64 = v_i21.wrapping_add(v_i18);
    let v__sh7: u64 = v_i24.wrapping_shr((0xau64) as u32);
    let v_i28: bool = (v_i24 < 0x400u64);
    let v__m9: u64 = (0u64.wrapping_sub((v_i28) as u64));
    let v__n10: u64 = (v__m9 ^ 0xffffffffffffffffu64);
    let v_i31: u64 = (v_i18 & v__n10);
    let v_i32: u64 = v__sh7.wrapping_add(v_i31);
    let v__n11: bool = (v_i2 ^ true);
    let v__m12: u64 = (0u64.wrapping_sub((v__n11) as u64));
    let v__a13: u64 = (v_i8 & v__m12);
    let v__m15: u64 = (0u64.wrapping_sub((v_i15) as u64));
    let v__a16: u64 = (v_i22 & v__m15);
    let v__o17: u64 = (v__a13 | v__a16);
    let v__n18: bool = (v_i15 ^ true);
    let v__c19: bool = (v__n18 & v_i2);
    let v__m20: u64 = (0u64.wrapping_sub((v__c19) as u64));
    let v__a21: u64 = (v_i32 & v__m20);
    let v__o22: u64 = (v__o17 | v__a21);
    let v__a25: u64 = (v__o22 & v__m24);
    v__a25
}
