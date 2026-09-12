#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of remw_gpr_gpr_gpr_32__reg_a0__rust__native_first.
//   Concat(If(Extract(31, 0, v1) == 0, Extract(31, 31, v0), If(And(Extract(31, 0, v0) == 2147483648, Extract(31, 0, v1) == 4294967295), 0, Extract(31, 31, bvsrem_i(Extract(31, 0, v0), Extract(31, 0, v1))))), If(Extract(31, 0, v1) == 0, Extract(31, 31, v0), If(And(Extract(31, 0, v0) == 2147483648, Extract(31, 0, v1) == 4294967295), 0, Extract(31, 31, bvsrem_i(Extract(31, 0, v0), Extract(31, 0, v1))))), If(Extract(31, 0, v1) == 0, Extract(31, 31, v0), If(And(Extract(31, 0, v0) == 2147483648, Extract(31, 0, v1) == 4294967295), 0, Extract(31, 31, bvsrem_i(Extract(31, 0, v0), Extract(31, 0, v1))))), If(Extract(31, 0, v1) == 0, Extract(31, 31, v0), If(And(Extract(31, 0, v0) == 2147483648, Extract(31, 0, v1) == 4294967295), 0, Extract(31, 31, bvsrem_i(Extract(31, 0, v0), Extract(31, 0, v1))))), If(Extract(31, 0, v1) == 0, Extract(31, 31, v0), If(And(Extract(31, 0, v0) == 2147483648, Extract(31, 0, 
#[no_mangle]
pub extern "C" fn emu_remw_gpr_gpr_gpr_32__reg_a0__rust__native_first(a: u32, b: u32) -> u64
{
    let v0: u32 = (b as u32);
    let v1: u32 = (a as u32);
    let v2: u32 = ((({ let n1: i32 = ((((v1) as i32)) as i32); let d1: i32 = ((((v0) as i32)) as i32); unsafe { if d1 == 0 || (n1 == i32::MIN && d1 == -1) { core::hint::unreachable_unchecked(); } } n1 % d1 })) as u32);
    let v3: bool = (((v0) as u32) == ((0xffffffffu32) as u32));
    let v4: bool = (((v1) as u32) == ((0x80000000u32) as u32));
    let v5: bool = ((v4) && (v3));
    let v6: u32 = (if (v5) { ((0x0u32) as u32) } else { ((v2) as u32) });
    let v7: bool = (((v0) as u32) == ((0x0u32) as u32));
    let v8: u32 = (if (v7) { ((v1) as u32) } else { ((v6) as u32) });
    let v9: u32 = (((((v2) as u32) >> 31) as u32) & 0x1u32);
    let v10: u32 = (if (v5) { ((0x0u32) as u32) } else { ((v9) as u32) });
    let v11: u32 = (((((a as u32)) >> 31) as u32) & 0x1u32);
    let v12: u32 = (if (v7) { ((v11) as u32) } else { ((v10) as u32) });
    let v13: u64 = (((((v12) as u64) << 63) | (((v12) as u64) << 62) | (((v12) as u64) << 61) | (((v12) as u64) << 60) | (((v12) as u64) << 59) | (((v12) as u64) << 58) | (((v12) as u64) << 57) | (((v12) as u64) << 56) | (((v12) as u64) << 55) | (((v12) as u64) << 54) | (((v12) as u64) << 53) | (((v12) as u64) << 52) | (((v12) as u64) << 51) | (((v12) as u64) << 50) | (((v12) as u64) << 49) | (((v12) as u64) << 48) | (((v12) as u64) << 47) | (((v12) as u64) << 46) | (((v12) as u64) << 45) | (((v12) as u64) << 44) | (((v12) as u64) << 43) | (((v12) as u64) << 42) | (((v12) as u64) << 41) | (((v12) as u64) << 40) | (((v12) as u64) << 39) | (((v12) as u64) << 38) | (((v12) as u64) << 37) | (((v12) as u64) << 36) | (((v12) as u64) << 35) | (((v12) as u64) << 34) | (((v12) as u64) << 33) | (((v12) as u64) << 32) | ((v8) as u64)) as u64);
    ((v13) as u64)
}
