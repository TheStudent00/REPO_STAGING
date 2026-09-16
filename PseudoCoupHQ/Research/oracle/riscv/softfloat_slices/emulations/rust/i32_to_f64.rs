#![allow(non_snake_case, unused_parens, unused_imports, unused_variables, unused_comparisons, clippy::all)]
use crate::helpers::*;


pub fn i32_to_f64_rm1(v_arg: u32) -> u64 {
    let v_i: bool = (v_arg == 0x0u32);
    let v__n7: bool = (v_i ^ true);
    let v__m8: u64 = (0u64.wrapping_sub((v__n7) as u64));
    let v__k1: u32 = sf_abs_u32(v_arg);
    let v__k2: u32 = sf_ctlz_u32(v__k1);
    let v_i3: u32 = v__k2;
    let v_i12: u64 = ((v__k1) as u64);
    let v_i4: u32 = v_i3.wrapping_add(0x15u32);
    let v_i8: u32 = 0x41du32.wrapping_sub(v_i3);
    let v_i9: u64 = ((v_i8) as u64);
    let v__sh5: u64 = v_i9.wrapping_shl((0x34u64) as u32);
    let v_i13: u64 = ((v_i4) as u64);
    let v__sh6: u64 = v_i12.wrapping_shl((v_i13) as u32);
    let v_i14: u64 = v__sh6;
    let v__sh3: u32 = v_arg.wrapping_shr((0x1fu32) as u32);
    let v_i6: u64 = ((v__sh3) as u64);
    let v__sh4: u64 = v_i6.wrapping_shl((0x3fu64) as u32);
    let v_i11: u64 = (v__sh5 | v__sh4);
    let v_i15: u64 = v_i11.wrapping_add(v_i14);
    let v__a9: u64 = (v_i15 & v__m8);
    v__a9
}
