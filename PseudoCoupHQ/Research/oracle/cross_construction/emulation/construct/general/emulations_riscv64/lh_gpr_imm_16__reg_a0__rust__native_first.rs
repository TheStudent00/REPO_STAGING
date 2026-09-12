#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of lh_gpr_imm_16__reg_a0__rust__native_first.
//   Concat(Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15,
#[no_mangle]
pub extern "C" fn emu_lh_gpr_imm_16__reg_a0__rust__native_first(a: u16) -> u64
{
    let v0: u32 = (a as u32);
    let v1: u32 = (((((a as u32)) >> 15) as u32) & 0x1u32);
    let v2: u64 = (((((v1) as u64) << 63) | (((v1) as u64) << 62) | (((v1) as u64) << 61) | (((v1) as u64) << 60) | (((v1) as u64) << 59) | (((v1) as u64) << 58) | (((v1) as u64) << 57) | (((v1) as u64) << 56) | (((v1) as u64) << 55) | (((v1) as u64) << 54) | (((v1) as u64) << 53) | (((v1) as u64) << 52) | (((v1) as u64) << 51) | (((v1) as u64) << 50) | (((v1) as u64) << 49) | (((v1) as u64) << 48) | (((v1) as u64) << 47) | (((v1) as u64) << 46) | (((v1) as u64) << 45) | (((v1) as u64) << 44) | (((v1) as u64) << 43) | (((v1) as u64) << 42) | (((v1) as u64) << 41) | (((v1) as u64) << 40) | (((v1) as u64) << 39) | (((v1) as u64) << 38) | (((v1) as u64) << 37) | (((v1) as u64) << 36) | (((v1) as u64) << 35) | (((v1) as u64) << 34) | (((v1) as u64) << 33) | (((v1) as u64) << 32) | (((v1) as u64) << 31) | (((v1) as u64) << 30) | (((v1) as u64) << 29) | (((v1) as u64) << 28) | (((v1) as u64) << 27) | (((v1) as u64) << 26) | (((v1) as u64) << 25) | (((v1) as u64) << 24) | (((v1) as u64) << 23) | (((v1) as u64) << 22) | (((v1) as u64) << 21) | (((v1) as u64) << 20) | (((v1) as u64) << 19) | (((v1) as u64) << 18) | (((v1) as u64) << 17) | (((v1) as u64) << 16) | ((v0) as u64)) as u64);
    ((v2) as u64)
}
