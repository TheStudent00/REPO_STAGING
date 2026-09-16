#![allow(non_snake_case, unused_parens, unused_imports, unused_variables, unused_comparisons, clippy::all)]
use crate::helpers::*;


pub fn f32_to_i64_rm1(v_arg: u64) -> u64 {
    let v_i: u32 = ((v_arg) as u32);
    let v_i1: bool = (((v_i) as i32) < (0i32));
    let v_i2: u32 = v_i.wrapping_shr((0x17u32) as u32);
    let v_i4: u32 = (v_i2 & 0xffu32);
    let v_i3: u32 = (v_i & 0x7fffffu32);
    let v_i14: u32 = (v_i & 0x7f800000u32);
    let v_i15: bool = (v_i14 == 0x0u32);
    let v__m1: u32 = (0u32.wrapping_sub((v_i15) as u32));
    let v_i5: u32 = 0xbeu32.wrapping_sub(v_i4);
    let v_i6: bool = (v_i4 > 0xbeu32);
    let v_i16: u32 = (v_i3 | 0x800000u32);
    let v__a2: u32 = (v_i3 & v__m1);
    let v__n3: u32 = (v__m1 ^ 0xffffffffu32);
    let v__a4: u32 = (v_i16 & v__n3);
    let v_i17: u32 = (v__a2 | v__a4);
    let v_i18: u64 = ((v_i17) as u64);
    let v__sh5: u64 = v_i18.wrapping_shl((0x28u64) as u32);
    let v_i19: u64 = v__sh5;
    let v_i9: bool = (v_i3 != 0x0u32);
    let v_i20: bool = (v_i4 == 0xbeu32);
    let v__m8: u64 = (0u64.wrapping_sub((v_i20) as u64));
    let v_i8: bool = (v_i4 == 0xffu32);
    let v_i10: bool = (v_i9 & v_i8);
    let v__m28: u64 = (0u64.wrapping_sub((v_i10) as u64));
    let v_i21: bool = (v_i5 < 0x40u32);
    let v_i22: u64 = ((v_i5) as u64);
    let v__sh6: u64 = v_i19.wrapping_shr((v_i22) as u32);
    let v_i23: u64 = v__sh6;
    let v__m7: u64 = (0u64.wrapping_sub((v_i21) as u64));
    let v_i24: u64 = (v_i23 & v__m7);
    let v__a9: u64 = (v_i19 & v__m8);
    let v__n10: u64 = (v__m8 ^ 0xffffffffffffffffu64);
    let v__a11: u64 = (v_i24 & v__n10);
    let v_i25: u64 = (v__a9 | v__a11);
    let v_i26: u64 = 0x0u64.wrapping_sub(v_i25);
    let v__m12: u64 = (0u64.wrapping_sub((v_i1) as u64));
    let v__a13: u64 = (v_i26 & v__m12);
    let v__n14: u64 = (v__m12 ^ 0xffffffffffffffffu64);
    let v__a15: u64 = (v_i25 & v__n14);
    let v_i27: u64 = (v__a13 | v__a15);
    let v_i28: bool = (v_i25 == 0x0u64);
    let v_i29: bool = (((v_i27) as i64) > (-1i64));
    let v_i30: bool = (v_i1 ^ v_i29);
    let v_i31: bool = (v_i28 | v_i30);
    let v__m20: u64 = (0u64.wrapping_sub((v_i31) as u64));
    let v__a21: u64 = (v_i27 & v__m20);
    let v__n22: u64 = (v__m20 ^ 0xffffffffffffffffu64);
    let v__a17: u64 = (0x8000000000000000u64 & v__m12);
    let v__a19: u64 = (0x7fffffffffffffffu64 & v__n14);
    let v_i32: u64 = (v__a17 | v__a19);
    let v__a23: u64 = (v_i32 & v__n22);
    let v_spec_select: u64 = (v__a21 | v__a23);
    let v__a29: u64 = (0x7fffffffffffffffu64 & v__m28);
    let v__n30: u64 = (v__m28 ^ 0xffffffffffffffffu64);
    let v__a31: u64 = (v_i32 & v__n30);
    let v_i12: u64 = (v__a29 | v__a31);
    let v__m32: u64 = (0u64.wrapping_sub((v_i6) as u64));
    let v__a33: u64 = (v_i12 & v__m32);
    let v__n34: bool = (v_i6 ^ true);
    let v__m35: u64 = (0u64.wrapping_sub((v__n34) as u64));
    let v__a36: u64 = (v_spec_select & v__m35);
    let v__o37: u64 = (v__a33 | v__a36);
    v__o37
}
