#![allow(non_snake_case, unused_parens, unused_imports, unused_variables, unused_comparisons, clippy::all)]
use crate::helpers::*;


pub fn f64_lt_rm0(v_arg: u64, v_arg1: u64) -> bool {
    let v_i: u64 = (v_arg & 0x7ff0000000000000u64);
    let v_i2: bool = (v_i != 0x7ff0000000000000u64);
    let v_i3: u64 = (v_arg & 0xfffffffffffffu64);
    let v_i4: bool = (v_i3 == 0x0u64);
    let v_i5: bool = (v_i2 | v_i4);
    let v_i7: u64 = (v_arg1 & 0x7ff0000000000000u64);
    let v_i8: bool = (v_i7 != 0x7ff0000000000000u64);
    let v_i9: u64 = (v_arg1 & 0xfffffffffffffu64);
    let v_i10: bool = (v_i9 == 0x0u64);
    let v_i11: bool = (v_i8 | v_i10);
    let v__c5: bool = (v_i5 & v_i11);
    let v_i13: u64 = (v_arg1 ^ v_arg);
    let v_i14: bool = (((v_i13) as i64) > (-1i64));
    let v_i16: bool = (((v_arg) as i64) < (0i64));
    let v_i17: u64 = (v_arg1 | v_arg);
    let v_i18: u64 = (v_i17 & 0x7fffffffffffffffu64);
    let v_i19: bool = (v_i18 != 0x0u64);
    let v_i20: bool = (v_i16 & v_i19);
    let v_i22: bool = (v_arg != v_arg1);
    let v_i23: bool = (v_arg < v_arg1);
    let v_i25: bool = (v_i16 ^ v_i23);
    let v_i26: bool = (v_i22 & v_i25);
    let v__a3: bool = (v_i26 & v_i14);
    let v__n1: bool = (v_i14 ^ true);
    let v__a2: bool = (v_i20 & v__n1);
    let v__o4: bool = (v__a2 | v__a3);
    let v__a6: bool = (v__o4 & v__c5);
    v__a6
}
