#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of ITYPE__op_ANDI__rd__rust__native_first.
//   
#[no_mangle]
pub extern "C" fn emu_ITYPE__op_ANDI__rd__rust__native_first(a: u64, b: u16) -> u64
{
    let v0: u32 = (((((b as u32)) >> 0) as u32) & 0xfffu32);
    let v1: u32 = (((!((v0) as u32)) as u32) & 0xfffu32);
    let v2: u32 = (((((b as u32)) >> 11) as u32) & 0x1u32);
    let v3: u32 = (((!((v2) as u32)) as u32) & 0x1u32);
    let v4: u64 = ((((((v3) as u64) << 62) | (((v3) as u64) << 61) | (((v3) as u64) << 60) | (((v3) as u64) << 59) | (((v3) as u64) << 58) | (((v3) as u64) << 57) | (((v3) as u64) << 56) | (((v3) as u64) << 55) | (((v3) as u64) << 54) | (((v3) as u64) << 53) | (((v3) as u64) << 52) | (((v3) as u64) << 51) | (((v3) as u64) << 50) | (((v3) as u64) << 49) | (((v3) as u64) << 48) | (((v3) as u64) << 47) | (((v3) as u64) << 46) | (((v3) as u64) << 45) | (((v3) as u64) << 44) | (((v3) as u64) << 43) | (((v3) as u64) << 42) | (((v3) as u64) << 41) | (((v3) as u64) << 40) | (((v3) as u64) << 39) | (((v3) as u64) << 38) | (((v3) as u64) << 37) | (((v3) as u64) << 36) | (((v3) as u64) << 35) | (((v3) as u64) << 34) | (((v3) as u64) << 33) | (((v3) as u64) << 32) | (((v3) as u64) << 31) | (((v3) as u64) << 30) | (((v3) as u64) << 29) | (((v3) as u64) << 28) | (((v3) as u64) << 27) | (((v3) as u64) << 26) | (((v3) as u64) << 25) | (((v3) as u64) << 24) | (((v3) as u64) << 23) | (((v3) as u64) << 22) | (((v3) as u64) << 21) | (((v3) as u64) << 20) | (((v3) as u64) << 19) | (((v3) as u64) << 18) | (((v3) as u64) << 17) | (((v3) as u64) << 16) | (((v3) as u64) << 15) | (((v3) as u64) << 14) | (((v3) as u64) << 13) | (((v3) as u64) << 12) | ((v1) as u64)) as u64) & 0x7fffffffffffffffu64);
    let v5: u64 = (((((a as u64)) >> 0) as u64) & 0x7fffffffffffffffu64);
    let v6: u64 = (((!((v5) as u64)) as u64) & 0x7fffffffffffffffu64);
    let v7: u64 = (((((v6) as u64) | ((v4) as u64)) as u64) & 0x7fffffffffffffffu64);
    let v8: u64 = (((!((v7) as u64)) as u64) & 0x7fffffffffffffffu64);
    let v9: u32 = (((((a as u64)) >> 63) as u32) & 0x1u32);
    let v10: u32 = (((!((v9) as u32)) as u32) & 0x1u32);
    let v11: u32 = (((((v3) as u32) | ((v10) as u32)) as u32) & 0x1u32);
    let v12: u32 = (((!((v11) as u32)) as u32) & 0x1u32);
    let v13: u64 = (((((v12) as u64) << 63) | ((v8) as u64)) as u64);
    ((v13) as u64)
}
