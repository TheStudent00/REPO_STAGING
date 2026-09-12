#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of flw_fpr_fpr_32__freg_fa0__rust__all_constructed.
//   Concat(4294967295, Extract(31, 0, v0))
#[no_mangle]
pub extern "C" fn emu_flw_fpr_fpr_32__freg_fa0__rust__all_constructed(a: u32) -> u64
{
    let v0: u32 = (a as u32);
    let v1: u32 = v0;
    let v2: u32 = 0xffffffffu32;
    let v3: u64 = (((((v2) as u64) << 32) | ((v1) as u64)) as u64);
    ((v3) as u64)
}
