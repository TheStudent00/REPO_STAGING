#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of ZBS_IOP__op_BSETI__rd__rust__native_first.
//   
#[no_mangle]
pub extern "C" fn emu_ZBS_IOP__op_BSETI__rd__rust__native_first(a: u64, b: u8) -> u64
{
    let v0: u32 = (((((b as u32)) >> 0) as u32) & 0x3fu32);
    let v1: u64 = (((((0x0u64) as u64) << 6) | ((v0) as u64)) as u64);
    let v2: u64 = ((((0x1u64) as u64).wrapping_shl((((v1) as u64) as u32))) as u64);
    let v3: u64 = ((((v2) as u64) | (((a as u64)) as u64)) as u64);
    ((v3) as u64)
}
