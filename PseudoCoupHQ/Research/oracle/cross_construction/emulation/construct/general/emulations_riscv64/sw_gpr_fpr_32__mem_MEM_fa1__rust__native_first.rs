#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of sw_gpr_fpr_32__mem_MEM_fa1__rust__native_first.
//   Concat(Extract(63, 32, v0), Extract(31, 0, v1))
#[no_mangle]
pub extern "C" fn emu_sw_gpr_fpr_32__mem_MEM_fa1__rust__native_first(a: u64, b: u32) -> u64
{
    let v0: u32 = (b as u32);
    let v1: u32 = ((((a as u64)) >> 32) as u32);
    let v2: u64 = (((((v1) as u64) << 32) | ((v0) as u64)) as u64);
    ((v2) as u64)
}
