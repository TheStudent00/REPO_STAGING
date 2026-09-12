#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of addw_gpr_gpr_gpr_32__reg_a0__rust__native_first.
//   Concat(Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract
#[no_mangle]
pub extern "C" fn emu_addw_gpr_gpr_gpr_32__reg_a0__rust__native_first(a: u32, b: u32) -> u64
{
    let v0: u32 = (b as u32);
    let v1: u32 = (a as u32);
    let v2: u32 = (((((v1) as u32)).wrapping_add(((v0) as u32))) as u32);
    let v3: u32 = (((((v2) as u32) >> 31) as u32) & 0x1u32);
    let v4: u64 = (((((v3) as u64) << 63) | (((v3) as u64) << 62) | (((v3) as u64) << 61) | (((v3) as u64) << 60) | (((v3) as u64) << 59) | (((v3) as u64) << 58) | (((v3) as u64) << 57) | (((v3) as u64) << 56) | (((v3) as u64) << 55) | (((v3) as u64) << 54) | (((v3) as u64) << 53) | (((v3) as u64) << 52) | (((v3) as u64) << 51) | (((v3) as u64) << 50) | (((v3) as u64) << 49) | (((v3) as u64) << 48) | (((v3) as u64) << 47) | (((v3) as u64) << 46) | (((v3) as u64) << 45) | (((v3) as u64) << 44) | (((v3) as u64) << 43) | (((v3) as u64) << 42) | (((v3) as u64) << 41) | (((v3) as u64) << 40) | (((v3) as u64) << 39) | (((v3) as u64) << 38) | (((v3) as u64) << 37) | (((v3) as u64) << 36) | (((v3) as u64) << 35) | (((v3) as u64) << 34) | (((v3) as u64) << 33) | (((v3) as u64) << 32) | ((v2) as u64)) as u64);
    ((v4) as u64)
}
