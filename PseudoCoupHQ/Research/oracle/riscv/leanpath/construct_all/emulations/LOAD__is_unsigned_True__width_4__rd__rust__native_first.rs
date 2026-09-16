#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of LOAD__is_unsigned_True__width_4__rd__rust__native_first.
//   
#[no_mangle]
pub extern "C" fn emu_LOAD__is_unsigned_True__width_4__rd__rust__native_first(a: u32) -> u64
{
    let v0: u32 = (a as u32);
    let v1: u64 = (((((0x0u32) as u64) << 32) | ((v0) as u64)) as u64);
    ((v1) as u64)
}
