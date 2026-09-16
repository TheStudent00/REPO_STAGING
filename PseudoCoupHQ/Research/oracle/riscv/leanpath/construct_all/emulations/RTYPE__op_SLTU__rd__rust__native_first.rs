#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of RTYPE__op_SLTU__rd__rust__native_first.
//   
#[no_mangle]
pub extern "C" fn emu_RTYPE__op_SLTU__rd__rust__native_first(a: u64, b: u64) -> u64
{
    let v0: bool = (((((b as u64)) as u64)) <= ((((a as u64)) as u64)));
    let v1: u32 = (if (v0) { ((0x0u32) as u32) } else { ((0x1u32) as u32) });
    let v2: u64 = (((((0x0u64) as u64) << 1) | ((v1) as u64)) as u64);
    ((v2) as u64)
}
