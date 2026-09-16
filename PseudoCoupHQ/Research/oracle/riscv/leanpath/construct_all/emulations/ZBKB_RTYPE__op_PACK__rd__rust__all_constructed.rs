#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of ZBKB_RTYPE__op_PACK__rd__rust__all_constructed.
//   
#[no_mangle]
pub extern "C" fn emu_ZBKB_RTYPE__op_PACK__rd__rust__all_constructed(a: u32, b: u32) -> u64
{
    let v0: u32 = (b as u32);
    let v1: u32 = (a as u32);
    let v2: u32 = v0;
    let v3: u32 = v1;
    let v4: u64 = (((((v3) as u64) << 32) | ((v2) as u64)) as u64);
    ((v4) as u64)
}
