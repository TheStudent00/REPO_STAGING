#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of lhu_gpr_mem_16__reg_a0__rust__all_constructed.
//   Concat(0, Extract(15, 0, v0))
#[no_mangle]
pub extern "C" fn emu_lhu_gpr_mem_16__reg_a0__rust__all_constructed(a: u16) -> u64
{
    let v0: u32 = (a as u32);
    let v1: u32 = v0;
    let v2: u64 = 0x0u64;
    let v3: u64 = (((((v2) as u64) << 16) | ((v1) as u64)) as u64);
    ((v3) as u64)
}
