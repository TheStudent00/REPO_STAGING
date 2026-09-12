#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of mulhu_gpr_gpr_same_64__reg_a0__rust__native_first.
//   Extract(127, 64, Concat(0, v0)*Concat(0, v0))
#[no_mangle]
pub extern "C" fn emu_mulhu_gpr_gpr_same_64__reg_a0__rust__native_first(a: u64) -> u64
{
    let v0: u128 = (((((0x0u64) as u128) << 64) | (((a as u64)) as u128)) as u128);
    let v1: u128 = (((((v0) as u128)).wrapping_mul(((v0) as u128))) as u128);
    let v2: u64 = ((((v1) as u128) >> 64) as u64);
    ((v2) as u64)
}
