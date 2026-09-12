#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of xor_gpr_gpr_gpr_64__reg_a0__rust__all_constructed.
//   v0 ^ v1
#[no_mangle]
pub extern "C" fn emu_xor_gpr_gpr_gpr_64__reg_a0__rust__all_constructed(a: u64, b: u64) -> u64
{
    let v0: u64 = (((((a as u64)) as u64) ^ (((b as u64)) as u64)) as u64);
    ((v0) as u64)
}
