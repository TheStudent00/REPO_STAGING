#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of ZBA_RTYPEUW__one__rd__rust__native_first.
//   
#[no_mangle]
pub extern "C" fn emu_ZBA_RTYPEUW__one__rd__rust__native_first(a: u32, b: u8, c: u64) -> u64
{
    let v0: u32 = (((((b as u32)) >> 0) as u32) & 0x3u32);
    let v1: u64 = (((((0x0u64) as u64) << 2) | ((v0) as u64)) as u64);
    let v2: u32 = (a as u32);
    let v3: u64 = (((((0x0u32) as u64) << 32) | ((v2) as u64)) as u64);
    let v4: u64 = ((((v3) as u64).wrapping_shl((((v1) as u64) as u32))) as u64);
    let v5: u64 = (((((v4) as u64)).wrapping_add((((c as u64)) as u64))) as u64);
    ((v5) as u64)
}
