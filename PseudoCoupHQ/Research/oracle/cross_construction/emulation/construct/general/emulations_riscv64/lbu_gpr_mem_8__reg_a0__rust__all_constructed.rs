#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of lbu_gpr_mem_8__reg_a0__rust__all_constructed.
//   Concat(0, Extract(7, 0, v0))
#[no_mangle]
pub extern "C" fn emu_lbu_gpr_mem_8__reg_a0__rust__all_constructed(a: u8) -> u64
{
    let v0: u32 = (a as u32);
    let v1: u32 = v0;
    let v2: u64 = 0x0u64;
    let v3: u64 = (((((v2) as u64) << 8) | ((v1) as u64)) as u64);
    ((v3) as u64)
}
