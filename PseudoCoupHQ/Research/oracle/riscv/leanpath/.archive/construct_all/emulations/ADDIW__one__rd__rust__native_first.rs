#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of ADDIW__one__rd__rust__native_first.
//   
#[no_mangle]
pub extern "C" fn emu_ADDIW__one__rd__rust__native_first(a: u32, b: u16) -> u64
{
    let v0: u32 = (a as u32);
    let v1: u32 = (((((b as u32)) >> 0) as u32) & 0xfffu32);
    let v2: u32 = (((((b as u32)) >> 11) as u32) & 0x1u32);
    let v3: u32 = (((((v2) as u32) << 31) | (((v2) as u32) << 30) | (((v2) as u32) << 29) | (((v2) as u32) << 28) | (((v2) as u32) << 27) | (((v2) as u32) << 26) | (((v2) as u32) << 25) | (((v2) as u32) << 24) | (((v2) as u32) << 23) | (((v2) as u32) << 22) | (((v2) as u32) << 21) | (((v2) as u32) << 20) | (((v2) as u32) << 19) | (((v2) as u32) << 18) | (((v2) as u32) << 17) | (((v2) as u32) << 16) | (((v2) as u32) << 15) | (((v2) as u32) << 14) | (((v2) as u32) << 13) | (((v2) as u32) << 12) | ((v1) as u32)) as u32);
    let v4: u32 = (((((v3) as u32)).wrapping_add(((v0) as u32))) as u32);
    let v5: u32 = (((((v4) as u32) >> 31) as u32) & 0x1u32);
    let v6: u64 = (((((v5) as u64) << 63) | (((v5) as u64) << 62) | (((v5) as u64) << 61) | (((v5) as u64) << 60) | (((v5) as u64) << 59) | (((v5) as u64) << 58) | (((v5) as u64) << 57) | (((v5) as u64) << 56) | (((v5) as u64) << 55) | (((v5) as u64) << 54) | (((v5) as u64) << 53) | (((v5) as u64) << 52) | (((v5) as u64) << 51) | (((v5) as u64) << 50) | (((v5) as u64) << 49) | (((v5) as u64) << 48) | (((v5) as u64) << 47) | (((v5) as u64) << 46) | (((v5) as u64) << 45) | (((v5) as u64) << 44) | (((v5) as u64) << 43) | (((v5) as u64) << 42) | (((v5) as u64) << 41) | (((v5) as u64) << 40) | (((v5) as u64) << 39) | (((v5) as u64) << 38) | (((v5) as u64) << 37) | (((v5) as u64) << 36) | (((v5) as u64) << 35) | (((v5) as u64) << 34) | (((v5) as u64) << 33) | (((v5) as u64) << 32) | ((v4) as u64)) as u64);
    ((v6) as u64)
}
