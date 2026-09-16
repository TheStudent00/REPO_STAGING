#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of REV8__one__rd__rust__native_first.
//   
#[no_mangle]
pub extern "C" fn emu_REV8__one__rd__rust__native_first(a: u64) -> u64
{
    let v0: u32 = (((((a as u64)) >> 56) as u32) & 0xffu32);
    let v1: u32 = (((((a as u64)) >> 48) as u32) & 0xffu32);
    let v2: u32 = (((((a as u64)) >> 40) as u32) & 0xffu32);
    let v3: u32 = (((((a as u64)) >> 32) as u32) & 0xffu32);
    let v4: u32 = (((((a as u64)) >> 24) as u32) & 0xffu32);
    let v5: u32 = (((((a as u64)) >> 16) as u32) & 0xffu32);
    let v6: u32 = (((((a as u64)) >> 8) as u32) & 0xffu32);
    let v7: u32 = (((((a as u64)) >> 0) as u32) & 0xffu32);
    let v8: u64 = (((((v7) as u64) << 56) | (((v6) as u64) << 48) | (((v5) as u64) << 40) | (((v4) as u64) << 32) | (((v3) as u64) << 24) | (((v2) as u64) << 16) | (((v1) as u64) << 8) | ((v0) as u64)) as u64);
    ((v8) as u64)
}
