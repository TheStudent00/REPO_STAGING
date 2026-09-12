#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of lhu_gpr_fpr_16__reg_a0__rust__native_first.
//   Concat(0, Extract(15, 0, v0))
#[no_mangle]
pub extern "C" fn emu_lhu_gpr_fpr_16__reg_a0__rust__native_first(a: u16) -> u64
{
    let v0: u32 = (a as u32);
    let v1: u64 = (((((0x0u64) as u64) << 16) | ((v0) as u64)) as u64);
    ((v1) as u64)
}
