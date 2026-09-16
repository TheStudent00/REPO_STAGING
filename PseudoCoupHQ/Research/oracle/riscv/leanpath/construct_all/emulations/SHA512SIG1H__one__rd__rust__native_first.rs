#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of SHA512SIG1H__one__rd__rust__native_first.
//   
#[no_mangle]
pub extern "C" fn emu_SHA512SIG1H__one__rd__rust__native_first(a: u64, b: u64) -> u64
{
    let v0: u32 = (((((a as u64)) >> 6) as u32) & 0x7u32);
    let v1: u32 = (((((b as u64)) >> 29) as u32) & 0x7u32);
    let v2: u32 = (((((a as u64)) >> 19) as u32) & 0x7u32);
    let v3: u32 = (((((v2) as u32) ^ ((v1) as u32) ^ ((v0) as u32)) as u32) & 0x7u32);
    let v4: u32 = (((((a as u64)) >> 0) as u32) & 0x3ffu32);
    let v5: u32 = (((((b as u64)) >> 32) as u32) & 0x3ffu32);
    let v6: u32 = (((((a as u64)) >> 22) as u32) & 0x3ffu32);
    let v7: u32 = (((((a as u64)) >> 9) as u32) & 0x3ffu32);
    let v8: u32 = (((((v7) as u32) ^ ((v6) as u32) ^ ((v5) as u32) ^ ((v4) as u32)) as u32) & 0x3ffu32);
    let v9: u32 = (((((b as u64)) >> 42) as u32) & 0x3fffffu32);
    let v10: u32 = (((((a as u64)) >> 32) as u32) & 0x3fffffu32);
    let v11: u32 = (((((a as u64)) >> 19) as u32) & 0x3fffffu32);
    let v12: u32 = (((((a as u64)) >> 10) as u32) & 0x3fffffu32);
    let v13: u32 = (((((b as u64)) >> 0) as u32) & 0x3fffffu32);
    let v14: u32 = (((((v13) as u32) ^ ((v12) as u32) ^ ((v11) as u32) ^ ((v10) as u32) ^ ((v9) as u32)) as u32) & 0x3fffffu32);
    let v15: u32 = (((((a as u64)) >> 54) as u32) & 0x3ffu32);
    let v16: u32 = (((((a as u64)) >> 41) as u32) & 0x3ffu32);
    let v17: u32 = (((((a as u64)) >> 32) as u32) & 0x3ffu32);
    let v18: u32 = (((((b as u64)) >> 22) as u32) & 0x3ffu32);
    let v19: u32 = (((((v18) as u32) ^ ((v17) as u32) ^ ((v16) as u32) ^ ((v15) as u32)) as u32) & 0x3ffu32);
    let v20: u32 = (((((a as u64)) >> 51) as u32) & 0x1fffu32);
    let v21: u32 = (((((a as u64)) >> 42) as u32) & 0x1fffu32);
    let v22: u32 = (((((b as u64)) >> 32) as u32) & 0x1fffu32);
    let v23: u32 = (((((v22) as u32) ^ ((v21) as u32) ^ ((v20) as u32)) as u32) & 0x1fffu32);
    let v24: u32 = (((((a as u64)) >> 55) as u32) & 0x3fu32);
    let v25: u32 = (((((b as u64)) >> 45) as u32) & 0x3fu32);
    let v26: u32 = (((((v25) as u32) ^ ((v24) as u32)) as u32) & 0x3fu32);
    let v27: u64 = (((((v26) as u64) << 58) | (((v23) as u64) << 45) | (((v19) as u64) << 35) | (((v14) as u64) << 13) | (((v8) as u64) << 3) | ((v3) as u64)) as u64);
    ((v27) as u64)
}
