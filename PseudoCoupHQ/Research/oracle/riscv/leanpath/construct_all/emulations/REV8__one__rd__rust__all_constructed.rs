#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of REV8__one__rd__rust__all_constructed.
//   
#[no_mangle]
pub extern "C" fn emu_REV8__one__rd__rust__all_constructed(a: u64) -> u64
{
    let v0: u32 = (((((a as u64)) >> 56) as u32) & 0xffu32);
    let v1: u32 = (((((a as u64)) >> 48) as u32) & 0xffu32);
    let v2: u32 = (((((a as u64)) >> 40) as u32) & 0xffu32);
    let v3: u32 = (((((a as u64)) >> 32) as u32) & 0xffu32);
    let v4: u32 = (((((a as u64)) >> 24) as u32) & 0xffu32);
    let v5: u32 = (((((a as u64)) >> 16) as u32) & 0xffu32);
    let v6: u32 = (((((a as u64)) >> 8) as u32) & 0xffu32);
    let v7: u32 = (((((a as u64)) >> 0) as u32) & 0xffu32);
    let v8: u32 = v0;
    let v9: u32 = v1;
    let v10: u32 = v2;
    let v11: u32 = v3;
    let v12: u32 = v4;
    let v13: u32 = v5;
    let v14: u32 = v6;
    let v15: u32 = v7;
    let v16: u32 = ((((((v15) as u32) << 8) | ((v14) as u32)) as u32) & 0xffffu32);
    let v17: u32 = ((((((v16) as u32) << 8) | ((v13) as u32)) as u32) & 0xffffffu32);
    let v18: u32 = (((((v17) as u32) << 8) | ((v12) as u32)) as u32);
    let v19: u64 = ((((((v18) as u64) << 8) | ((v11) as u64)) as u64) & 0xffffffffffu64);
    let v20: u64 = ((((((v19) as u64) << 8) | ((v10) as u64)) as u64) & 0xffffffffffffu64);
    let v21: u64 = ((((((v20) as u64) << 8) | ((v9) as u64)) as u64) & 0xffffffffffffffu64);
    let v22: u64 = (((((v21) as u64) << 8) | ((v8) as u64)) as u64);
    ((v22) as u64)
}
