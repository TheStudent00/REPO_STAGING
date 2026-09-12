#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of sb_gpr_gpr_8__mem_MEM_a1__rust__all_constructed.
//   Concat(Extract(63, 8, v0), Extract(7, 0, v1))
#[no_mangle]
pub extern "C" fn emu_sb_gpr_gpr_8__mem_MEM_a1__rust__all_constructed(a: u64, b: u8) -> u64
{
    let v0: u32 = (b as u32);
    let v1: u64 = (((((a as u64)) >> 8) as u64) & 0xffffffffffffffu64);
    let v2: u32 = v0;
    let v3: u64 = v1;
    let v4: u64 = (((((v3) as u64) << 8) | ((v2) as u64)) as u64);
    ((v4) as u64)
}
