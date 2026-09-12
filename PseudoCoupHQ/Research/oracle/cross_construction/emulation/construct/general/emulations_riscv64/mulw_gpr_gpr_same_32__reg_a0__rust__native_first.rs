#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of mulw_gpr_gpr_same_32__reg_a0__rust__native_first.
//   Concat(Extract(31, 31, Extract(31, 0, v0)*Extract(31, 0, v0)), Extract(31, 31, Extract(31, 0, v0)*Extract(31, 0, v0)), Extract(31, 31, Extract(31, 0, v0)*Extract(31, 0, v0)), Extract(31, 31, Extract(31, 0, v0)*Extract(31, 0, v0)), Extract(31, 31, Extract(31, 0, v0)*Extract(31, 0, v0)), Extract(31, 31, Extract(31, 0, v0)*Extract(31, 0, v0)), Extract(31, 31, Extract(31, 0, v0)*Extract(31, 0, v0)), Extract(31, 31, Extract(31, 0, v0)*Extract(31, 0, v0)), Extract(31, 31, Extract(31, 0, v0)*Extract(31, 0, v0)), Extract(31, 31, Extract(31, 0, v0)*Extract(31, 0, v0)), Extract(31, 31, Extract(31, 0, v0)*Extract(31, 0, v0)), Extract(31, 31, Extract(31, 0, v0)*Extract(31, 0, v0)), Extract(31, 31, Extract(31, 0, v0)*Extract(31, 0, v0)), Extract(31, 31, Extract(31, 0, v0)*Extract(31, 0, v0)), Extract(31, 31, Extract(31, 0, v0)*Extract(31, 0, v0)), Extract(31, 31, Extract(31, 0, v0)*Extract(31, 0, v0)
#[no_mangle]
pub extern "C" fn emu_mulw_gpr_gpr_same_32__reg_a0__rust__native_first(a: u32) -> u64
{
    let v0: u32 = (a as u32);
    let v1: u32 = (((((v0) as u32)).wrapping_mul(((v0) as u32))) as u32);
    let v2: u32 = (((((v1) as u32) >> 31) as u32) & 0x1u32);
    let v3: u64 = (((((v2) as u64) << 63) | (((v2) as u64) << 62) | (((v2) as u64) << 61) | (((v2) as u64) << 60) | (((v2) as u64) << 59) | (((v2) as u64) << 58) | (((v2) as u64) << 57) | (((v2) as u64) << 56) | (((v2) as u64) << 55) | (((v2) as u64) << 54) | (((v2) as u64) << 53) | (((v2) as u64) << 52) | (((v2) as u64) << 51) | (((v2) as u64) << 50) | (((v2) as u64) << 49) | (((v2) as u64) << 48) | (((v2) as u64) << 47) | (((v2) as u64) << 46) | (((v2) as u64) << 45) | (((v2) as u64) << 44) | (((v2) as u64) << 43) | (((v2) as u64) << 42) | (((v2) as u64) << 41) | (((v2) as u64) << 40) | (((v2) as u64) << 39) | (((v2) as u64) << 38) | (((v2) as u64) << 37) | (((v2) as u64) << 36) | (((v2) as u64) << 35) | (((v2) as u64) << 34) | (((v2) as u64) << 33) | (((v2) as u64) << 32) | ((v1) as u64)) as u64);
    ((v3) as u64)
}
