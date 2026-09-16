#![allow(non_snake_case, unused_parens, unused_imports, unused_variables, unused_comparisons, clippy::all)]
use crate::helpers::*;


pub fn f64_roundToInt_rm0(v_arg: u64, v_arg1: bool) -> u64 {
    let v_i: u64 = v_arg.wrapping_shr((0x34u64) as u32);
    let v_i2: u32 = ((v_i) as u32);
    let v_i3: u32 = (v_i2 & 0x7ffu32);
    let v_i4: bool = (v_i3 < 0x3ffu32);
    let v_i16: bool = (v_i3 > 0x432u32);
    let v_i6: u64 = (v_arg & 0x7fffffffffffffffu64);
    let v_i7: bool = (v_i6 == 0x0u64);
    let v_i18: bool = (v_i3 != 0x7ffu32);
    let v_i19: u64 = (v_arg & 0xfffffffffffffu64);
    let v_i20: bool = (v_i19 == 0x0u64);
    let v_i21: bool = (v_i20 | v_i18);
    let v__m1: u64 = (0u64.wrapping_sub((v_i21) as u64));
    let v__a2: u64 = (v_arg & v__m1);
    let v__n3: u64 = (v__m1 ^ 0xffffffffffffffffu64);
    let v__a4: u64 = (0x7ff8000000000000u64 & v__n3);
    let v_spec_select4: u64 = (v__a2 | v__a4);
    let v_i23: u32 = 0x433u32.wrapping_sub(v_i3);
    let v_i24: u64 = ((v_i23) as u64);
    let v__sh5: u64 = 0x1u64.wrapping_shl((v_i24) as u32);
    let v_i25: u64 = v__sh5;
    let v_i12: bool = (v_i3 == 0x3feu32);
    let v_i26: u64 = v_i25.wrapping_add(0xffffffffffffffffu64);
    let v__sh6: u64 = v_i25.wrapping_shr((0x1u64) as u32);
    let v_i28: u64 = v__sh6.wrapping_add(v_arg);
    let v_i29: u64 = (v_i28 & v_i26);
    let v_i30: bool = (v_i29 == 0x0u64);
    let v__m7: u64 = (0u64.wrapping_sub((v_i30) as u64));
    let v_i31: u64 = (v_i25 ^ 0xffffffffffffffffu64);
    let v__a8: u64 = (v_i31 & v__m7);
    let v__n9: u64 = (v__m7 ^ 0xffffffffffffffffu64);
    let v_i32: u64 = (v__a8 | v__n9);
    let v_i33: u64 = 0x0u64.wrapping_sub(v_i25);
    let v_i34: u64 = (v_i32 & v_i33);
    let v_i35: u64 = (v_i34 & v_i28);
    let v_i9: u64 = (v_arg & 0x8000000000000000u64);
    let v_i11: bool = (v_i19 != 0x0u64);
    let v_i13: bool = (v_i11 & v_i12);
    let v__m11: u64 = (0u64.wrapping_sub((v_i13) as u64));
    let v_i14: u64 = (v_i9 | 0x3ff0000000000000u64);
    let v__a12: u64 = (v_i14 & v__m11);
    let v__n13: u64 = (v__m11 ^ 0xffffffffffffffffu64);
    let v__a14: u64 = (v_i9 & v__n13);
    let v_spec_select: u64 = (v__a12 | v__a14);
    let v__c15: bool = (v_i7 & v_i4);
    let v__m16: u64 = (0u64.wrapping_sub((v__c15) as u64));
    let v__a17: u64 = (v_arg & v__m16);
    let v__n18: bool = (v_i7 ^ true);
    let v__c19: bool = (v__n18 & v_i4);
    let v__m20: u64 = (0u64.wrapping_sub((v__c19) as u64));
    let v__a21: u64 = (v_spec_select & v__m20);
    let v__o22: u64 = (v__a17 | v__a21);
    let v__n23: bool = (v_i4 ^ true);
    let v__n24: bool = (v_i16 ^ true);
    let v__c25: bool = (v__n23 & v__n24);
    let v__m26: u64 = (0u64.wrapping_sub((v__c25) as u64));
    let v__a27: u64 = (v_i35 & v__m26);
    let v__o28: u64 = (v__o22 | v__a27);
    let v__m30: u64 = (0u64.wrapping_sub((v_i16) as u64));
    let v__a31: u64 = (v_spec_select4 & v__m30);
    let v__o32: u64 = (v__o28 | v__a31);
    v__o32
}
