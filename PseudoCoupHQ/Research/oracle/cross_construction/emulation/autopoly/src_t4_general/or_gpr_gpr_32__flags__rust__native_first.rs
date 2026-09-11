#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of or_gpr_gpr_32__flags__rust__native_first.
//   Concat(Extract(31, 0, v0) | Extract(31, 0, v1), 0)
#[no_mangle]
pub extern "C" fn emu_or_gpr_gpr_32__flags__rust__native_first(a: u32, b: u32) -> u64
{
    let v0: u32 = (b as u32);
    let v1: u32 = (a as u32);
    let v2: u32 = ((((v1) as u32) | ((v0) as u32)) as u32);
    let v3: u64 = (((((v2) as u64) << 32) | ((0x0u32) as u64)) as u64);
    ((v3) as u64)
}
