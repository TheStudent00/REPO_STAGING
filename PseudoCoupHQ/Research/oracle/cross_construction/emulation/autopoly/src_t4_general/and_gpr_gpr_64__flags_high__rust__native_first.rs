#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of and_gpr_gpr_64__flags_high__rust__native_first.
//   ~(~v0 | ~v1)
#[no_mangle]
pub extern "C" fn emu_and_gpr_gpr_64__flags_high__rust__native_first(a: u64, b: u64) -> u64
{
    let v0: u64 = ((!(((b as u64)) as u64)) as u64);
    let v1: u64 = ((!(((a as u64)) as u64)) as u64);
    let v2: u64 = ((((v1) as u64) | ((v0) as u64)) as u64);
    let v3: u64 = ((!((v2) as u64)) as u64);
    ((v3) as u64)
}
