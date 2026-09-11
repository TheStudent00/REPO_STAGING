#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of and_gpr_gpr_32__flags__rust__all_constructed.
//   Concat(~(~Extract(31, 0, v0) | ~Extract(31, 0, v1)), 0)
#[no_mangle]
pub extern "C" fn emu_and_gpr_gpr_32__flags__rust__all_constructed(a: u32, b: u32) -> u64
{
    let v0: u32 = (b as u32);
    let v1: u32 = ((!((v0) as u32)) as u32);
    let v2: u32 = (a as u32);
    let v3: u32 = ((!((v2) as u32)) as u32);
    let v4: u32 = ((((v3) as u32) | ((v1) as u32)) as u32);
    let v5: u32 = ((!((v4) as u32)) as u32);
    let v6: u32 = 0x0u32;
    let v7: u32 = v5;
    let v8: u64 = (((((v7) as u64) << 32) | ((v6) as u64)) as u64);
    ((v8) as u64)
}
