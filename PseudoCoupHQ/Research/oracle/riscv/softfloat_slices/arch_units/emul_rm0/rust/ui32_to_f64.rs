#![allow(non_snake_case, unused_parens, unused_imports, unused_variables, unused_comparisons, clippy::all)]
use crate::helpers::*;


pub fn ui32_to_f64_rm0(v_arg: u32) -> u64 {
    let v_i: bool = (v_arg == 0x0u32);
    let v__n4: bool = (v_i ^ true);
    let v__m5: u64 = (0u64.wrapping_sub((v__n4) as u64));
    let v__k1: u32 = sf_ctlz_u32(v_arg);
    let v_i2: u32 = v__k1;
    let v_i3: u32 = v_i2.wrapping_add(0x15u32);
    let v_i4: u32 = 0x41du32.wrapping_sub(v_i2);
    let v_i5: u64 = ((v_i4) as u64);
    let v__sh2: u64 = v_i5.wrapping_shl((0x34u64) as u32);
    let v_i8: u64 = ((v_i3) as u64);
    let v_i7: u64 = ((v_arg) as u64);
    let v__sh3: u64 = v_i7.wrapping_shl((v_i8) as u32);
    let v_i9: u64 = v__sh3;
    let v_i10: u64 = v__sh2.wrapping_add(v_i9);
    let v__a6: u64 = (v_i10 & v__m5);
    v__a6
}
