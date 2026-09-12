#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of sub_gpr_gpr_gpr_64__reg_a0__rust__native_first.
//   v0*18446744073709551615 + v1
#[no_mangle]
pub extern "C" fn emu_sub_gpr_gpr_gpr_64__reg_a0__rust__native_first(a: u64, b: u64) -> u64
{
    let v0: u64 = ((((((b as u64)) as u64)).wrapping_mul(((0xffffffffffffffffu64) as u64))) as u64);
    let v1: u64 = (((((v0) as u64)).wrapping_add((((a as u64)) as u64))) as u64);
    ((v1) as u64)
}
