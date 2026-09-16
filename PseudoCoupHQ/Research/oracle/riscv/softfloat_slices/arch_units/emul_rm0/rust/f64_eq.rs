#![allow(non_snake_case, unused_parens, unused_imports, unused_variables, unused_comparisons, clippy::all)]
use crate::helpers::*;


pub fn f64_eq_rm0(v_arg: u64, v_arg1: u64) -> bool {
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
    let v__c1: bool = (v_i5 & v_i11);
    let v_i13: bool = (v_arg == v_arg1);
    let v_i14: u64 = (v_arg1 | v_arg);
    let v_i15: u64 = (v_i14 & 0x7fffffffffffffffu64);
    let v_i16: bool = (v_i15 == 0x0u64);
    let v_i17: bool = (v_i13 | v_i16);
    let v__a2: bool = (v_i17 & v__c1);
    v__a2
}
