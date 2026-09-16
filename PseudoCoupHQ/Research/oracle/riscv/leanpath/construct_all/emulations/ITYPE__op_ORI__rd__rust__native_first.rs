#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of ITYPE__op_ORI__rd__rust__native_first.
//   
#[no_mangle]
pub extern "C" fn emu_ITYPE__op_ORI__rd__rust__native_first(a: u64, b: u16) -> u64
{
    let v0: u64 = (((((a as u64)) >> 0) as u64) & 0x3fffffffffffffffu64);
    let v1: u32 = (((((b as u32)) >> 0) as u32) & 0xfffu32);
    let v2: u32 = (((((b as u32)) >> 11) as u32) & 0x1u32);
    let v3: u64 = ((((((v2) as u64) << 61) | (((v2) as u64) << 60) | (((v2) as u64) << 59) | (((v2) as u64) << 58) | (((v2) as u64) << 57) | (((v2) as u64) << 56) | (((v2) as u64) << 55) | (((v2) as u64) << 54) | (((v2) as u64) << 53) | (((v2) as u64) << 52) | (((v2) as u64) << 51) | (((v2) as u64) << 50) | (((v2) as u64) << 49) | (((v2) as u64) << 48) | (((v2) as u64) << 47) | (((v2) as u64) << 46) | (((v2) as u64) << 45) | (((v2) as u64) << 44) | (((v2) as u64) << 43) | (((v2) as u64) << 42) | (((v2) as u64) << 41) | (((v2) as u64) << 40) | (((v2) as u64) << 39) | (((v2) as u64) << 38) | (((v2) as u64) << 37) | (((v2) as u64) << 36) | (((v2) as u64) << 35) | (((v2) as u64) << 34) | (((v2) as u64) << 33) | (((v2) as u64) << 32) | (((v2) as u64) << 31) | (((v2) as u64) << 30) | (((v2) as u64) << 29) | (((v2) as u64) << 28) | (((v2) as u64) << 27) | (((v2) as u64) << 26) | (((v2) as u64) << 25) | (((v2) as u64) << 24) | (((v2) as u64) << 23) | (((v2) as u64) << 22) | (((v2) as u64) << 21) | (((v2) as u64) << 20) | (((v2) as u64) << 19) | (((v2) as u64) << 18) | (((v2) as u64) << 17) | (((v2) as u64) << 16) | (((v2) as u64) << 15) | (((v2) as u64) << 14) | (((v2) as u64) << 13) | (((v2) as u64) << 12) | ((v1) as u64)) as u64) & 0x3fffffffffffffffu64);
    let v4: u64 = (((((v3) as u64) | ((v0) as u64)) as u64) & 0x3fffffffffffffffu64);
    let v5: u32 = (((((a as u64)) >> 62) as u32) & 0x1u32);
    let v6: u32 = (((((v2) as u32) | ((v5) as u32)) as u32) & 0x1u32);
    let v7: u32 = (((((a as u64)) >> 63) as u32) & 0x1u32);
    let v8: u32 = (((((v2) as u32) | ((v7) as u32)) as u32) & 0x1u32);
    let v9: u64 = (((((v8) as u64) << 63) | (((v6) as u64) << 62) | ((v4) as u64)) as u64);
    ((v9) as u64)
}
