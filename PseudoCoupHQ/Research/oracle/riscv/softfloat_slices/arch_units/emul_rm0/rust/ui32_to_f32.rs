#![allow(non_snake_case, unused_parens, unused_imports, unused_variables, unused_comparisons, clippy::all)]
use crate::helpers::*;


pub fn ui32_to_f32_rm0(v_arg: u32) -> u64 {
    let v_i: bool = (v_arg == 0x0u32);
    let v__n25: bool = (v_i ^ true);
    let v__m26: u32 = (0u32.wrapping_sub((v__n25) as u32));
    let v_i2: bool = (((v_arg) as i32) > (-1i32));
    let v__k1: u32 = sf_ctlz_u32(v_arg);
    let v_i17: u32 = v__k1;
    let v_i18: u8 = ((v_i17) as u8);
    let v_i19: u8 = v_i18.wrapping_add(0xffu8);
    let v_i20: u32 = ((v_i19) as u32);
    let v_i21: u16 = ((v_i19) as u16);
    let v_i22: u16 = 0x9cu16.wrapping_sub(v_i21);
    let v_i23: bool = (v_arg < 0x1000000u32);
    let v__sh2: u32 = v_arg.wrapping_shr((0x1u32) as u32);
    let v_i4: u32 = (v_arg & 0x1u32);
    let v_i5: u32 = v__sh2.wrapping_add(0x40u32);
    let v__sh3: u32 = v_i5.wrapping_shr((0x7u32) as u32);
    let v__masked: u32 = (v__sh2 & 0x7fu32);
    let v_i7: u32 = (v__masked | v_i4);
    let v_i9: bool = (v_i7 == 0x40u32);
    let v_i10: u32 = ((v_i9) as u32);
    let v_i11: u32 = (v_i10 ^ 0xffffffffu32);
    let v_i12: u32 = (v__sh3 & v_i11);
    let v_i13: bool = (v_i12 == 0x0u32);
    let v__m4: u32 = (0u32.wrapping_sub((v_i13) as u32));
    let v__n5: u32 = (v__m4 ^ 0xffffffffu32);
    let v_i14: u32 = (0x4e800000u32 & v__n5);
    let v_i15: u32 = v_i12.wrapping_add(v_i14);
    let v_i25: u32 = ((v_i22) as u32);
    let v__sh6: u32 = v_i25.wrapping_shl((0x17u32) as u32);
    let v_i26: u32 = v__sh6;
    let v_i27: u32 = v_i20.wrapping_add(0xfffffff9u32);
    let v__sh7: u32 = v_arg.wrapping_shl((v_i27) as u32);
    let v_i28: u32 = v__sh7;
    let v_i29: u32 = v_i28.wrapping_add(v_i26);
    let v__sh8: u32 = v_arg.wrapping_shl((v_i20) as u32);
    let v_i30: u32 = v__sh8;
    let v_i31: u32 = v_i30.wrapping_add(0x40u32);
    let v__sh9: u32 = v_i31.wrapping_shr((0x7u32) as u32);
    let v_i33: u32 = (v_i30 & 0x7fu32);
    let v_i35: bool = (v_i33 == 0x40u32);
    let v_i36: u32 = ((v_i35) as u32);
    let v_i37: u32 = (v_i36 ^ 0xffffffffu32);
    let v_i38: u32 = (v__sh9 & v_i37);
    let v_i39: bool = (v_i38 == 0x0u32);
    let v__m11: u32 = (0u32.wrapping_sub((v_i39) as u32));
    let v__n12: u32 = (v__m11 ^ 0xffffffffu32);
    let v_i42: u32 = (v_i26 & v__n12);
    let v_i43: u32 = v_i38.wrapping_add(v_i42);
    let v__n13: bool = (v_i2 ^ true);
    let v__m14: u32 = (0u32.wrapping_sub((v__n13) as u32));
    let v__a15: u32 = (v_i15 & v__m14);
    let v__m17: u32 = (0u32.wrapping_sub((v_i23) as u32));
    let v__a18: u32 = (v_i29 & v__m17);
    let v__o19: u32 = (v__a15 | v__a18);
    let v__n20: bool = (v_i23 ^ true);
    let v__c21: bool = (v_i2 & v__n20);
    let v__m22: u32 = (0u32.wrapping_sub((v__c21) as u32));
    let v__a23: u32 = (v_i43 & v__m22);
    let v__o24: u32 = (v__o19 | v__a23);
    let v__a27: u32 = (v__o24 & v__m26);
    let v_i44: u64 = ((v__a27) as u64);
    v_i44
}
