#![allow(non_snake_case, unused_parens, unused_imports, unused_variables, unused_comparisons, clippy::all)]
use crate::helpers::*;


pub fn f64_roundToInt_rm1(v_arg: u64, v_arg1: bool) -> u64 {
    let v_i: u64 = v_arg.wrapping_shr((0x34u64) as u32);
    let v_i2: u32 = ((v_i) as u32);
    let v_i3: u32 = (v_i2 & 0x7ffu32);
    let v_i4: bool = (v_i3 < 0x3ffu32);
    let v_i6: u64 = (v_arg & 0x7fffffffffffffffu64);
    let v_i7: bool = (v_i6 == 0x0u64);
    let v__m1: u64 = (0u64.wrapping_sub((v_i7) as u64));
    let v_i8: u64 = (v_arg & 0x8000000000000000u64);
    let v__a2: u64 = (v_arg & v__m1);
    let v__n3: u64 = (v__m1 ^ 0xffffffffffffffffu64);
    let v__a4: u64 = (v_i8 & v__n3);
    let v_spec_select: u64 = (v__a2 | v__a4);
    let v_i10: bool = (v_i3 > 0x432u32);
    let v_i12: bool = (v_i3 != 0x7ffu32);
    let v_i17: u32 = 0x433u32.wrapping_sub(v_i3);
    let v_i18: u64 = ((v_i17) as u64);
    let v__sh9: u64 = 0xffffffffffffffffu64.wrapping_shl((v_i18) as u32);
    let v__neg: u64 = v__sh9;
    let v_i19: u64 = (v_arg & v__neg);
    let v_i13: u64 = (v_arg & 0xfffffffffffffu64);
    let v_i14: bool = (v_i13 == 0x0u64);
    let v_i15: bool = (v_i14 | v_i12);
    let v__m5: u64 = (0u64.wrapping_sub((v_i15) as u64));
    let v__a6: u64 = (v_arg & v__m5);
    let v__n7: u64 = (v__m5 ^ 0xffffffffffffffffu64);
    let v__a8: u64 = (0x7ff8000000000000u64 & v__n7);
    let v_spec_select4: u64 = (v__a6 | v__a8);
    let v__n10: bool = (v_i10 ^ true);
    let v__n11: bool = (v_i4 ^ true);
    let v__c12: bool = (v__n10 & v__n11);
    let v__m13: u64 = (0u64.wrapping_sub((v__c12) as u64));
    let v__a14: u64 = (v_i19 & v__m13);
    let v__m15: u64 = (0u64.wrapping_sub((v_i4) as u64));
    let v__a16: u64 = (v_spec_select & v__m15);
    let v__o17: u64 = (v__a14 | v__a16);
    let v__m19: u64 = (0u64.wrapping_sub((v_i10) as u64));
    let v__a20: u64 = (v_spec_select4 & v__m19);
    let v__o21: u64 = (v__o17 | v__a20);
    v__o21
}
