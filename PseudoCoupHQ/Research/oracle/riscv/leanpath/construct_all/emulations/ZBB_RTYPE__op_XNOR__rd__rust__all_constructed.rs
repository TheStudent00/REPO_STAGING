#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of ZBB_RTYPE__op_XNOR__rd__rust__all_constructed.
//   
#[no_mangle]
pub extern "C" fn emu_ZBB_RTYPE__op_XNOR__rd__rust__all_constructed(a: u64, b: u64) -> u64
{
    let v0: u64 = (((((a as u64)) as u64) ^ (((b as u64)) as u64)) as u64);
    let v1: u64 = ((!((v0) as u64)) as u64);
    ((v1) as u64)
}
