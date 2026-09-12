#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of lh_gpr_gpr_16__reg_a0__rust__all_constructed.
//   Concat(Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15,
#[no_mangle]
pub extern "C" fn emu_lh_gpr_gpr_16__reg_a0__rust__all_constructed(a: u16) -> u64
{
    let v0: u32 = (a as u32);
    let v1: u32 = (((((a as u32)) >> 15) as u32) & 0x1u32);
    let v2: u32 = v0;
    let v3: u32 = v1;
    let v4: u32 = ((((((v3) as u32) << 1) | ((v3) as u32)) as u32) & 0x3u32);
    let v5: u32 = ((((((v4) as u32) << 1) | ((v3) as u32)) as u32) & 0x7u32);
    let v6: u32 = ((((((v5) as u32) << 1) | ((v3) as u32)) as u32) & 0xfu32);
    let v7: u32 = ((((((v6) as u32) << 1) | ((v3) as u32)) as u32) & 0x1fu32);
    let v8: u32 = ((((((v7) as u32) << 1) | ((v3) as u32)) as u32) & 0x3fu32);
    let v9: u32 = ((((((v8) as u32) << 1) | ((v3) as u32)) as u32) & 0x7fu32);
    let v10: u32 = ((((((v9) as u32) << 1) | ((v3) as u32)) as u32) & 0xffu32);
    let v11: u32 = ((((((v10) as u32) << 1) | ((v3) as u32)) as u32) & 0x1ffu32);
    let v12: u32 = ((((((v11) as u32) << 1) | ((v3) as u32)) as u32) & 0x3ffu32);
    let v13: u32 = ((((((v12) as u32) << 1) | ((v3) as u32)) as u32) & 0x7ffu32);
    let v14: u32 = ((((((v13) as u32) << 1) | ((v3) as u32)) as u32) & 0xfffu32);
    let v15: u32 = ((((((v14) as u32) << 1) | ((v3) as u32)) as u32) & 0x1fffu32);
    let v16: u32 = ((((((v15) as u32) << 1) | ((v3) as u32)) as u32) & 0x3fffu32);
    let v17: u32 = ((((((v16) as u32) << 1) | ((v3) as u32)) as u32) & 0x7fffu32);
    let v18: u32 = ((((((v17) as u32) << 1) | ((v3) as u32)) as u32) & 0xffffu32);
    let v19: u32 = ((((((v18) as u32) << 1) | ((v3) as u32)) as u32) & 0x1ffffu32);
    let v20: u32 = ((((((v19) as u32) << 1) | ((v3) as u32)) as u32) & 0x3ffffu32);
    let v21: u32 = ((((((v20) as u32) << 1) | ((v3) as u32)) as u32) & 0x7ffffu32);
    let v22: u32 = ((((((v21) as u32) << 1) | ((v3) as u32)) as u32) & 0xfffffu32);
    let v23: u32 = ((((((v22) as u32) << 1) | ((v3) as u32)) as u32) & 0x1fffffu32);
    let v24: u32 = ((((((v23) as u32) << 1) | ((v3) as u32)) as u32) & 0x3fffffu32);
    let v25: u32 = ((((((v24) as u32) << 1) | ((v3) as u32)) as u32) & 0x7fffffu32);
    let v26: u32 = ((((((v25) as u32) << 1) | ((v3) as u32)) as u32) & 0xffffffu32);
    let v27: u32 = ((((((v26) as u32) << 1) | ((v3) as u32)) as u32) & 0x1ffffffu32);
    let v28: u32 = ((((((v27) as u32) << 1) | ((v3) as u32)) as u32) & 0x3ffffffu32);
    let v29: u32 = ((((((v28) as u32) << 1) | ((v3) as u32)) as u32) & 0x7ffffffu32);
    let v30: u32 = ((((((v29) as u32) << 1) | ((v3) as u32)) as u32) & 0xfffffffu32);
    let v31: u32 = ((((((v30) as u32) << 1) | ((v3) as u32)) as u32) & 0x1fffffffu32);
    let v32: u32 = ((((((v31) as u32) << 1) | ((v3) as u32)) as u32) & 0x3fffffffu32);
    let v33: u32 = ((((((v32) as u32) << 1) | ((v3) as u32)) as u32) & 0x7fffffffu32);
    let v34: u32 = (((((v33) as u32) << 1) | ((v3) as u32)) as u32);
    let v35: u64 = ((((((v34) as u64) << 1) | ((v3) as u64)) as u64) & 0x1ffffffffu64);
    let v36: u64 = ((((((v35) as u64) << 1) | ((v3) as u64)) as u64) & 0x3ffffffffu64);
    let v37: u64 = ((((((v36) as u64) << 1) | ((v3) as u64)) as u64) & 0x7ffffffffu64);
    let v38: u64 = ((((((v37) as u64) << 1) | ((v3) as u64)) as u64) & 0xfffffffffu64);
    let v39: u64 = ((((((v38) as u64) << 1) | ((v3) as u64)) as u64) & 0x1fffffffffu64);
    let v40: u64 = ((((((v39) as u64) << 1) | ((v3) as u64)) as u64) & 0x3fffffffffu64);
    let v41: u64 = ((((((v40) as u64) << 1) | ((v3) as u64)) as u64) & 0x7fffffffffu64);
    let v42: u64 = ((((((v41) as u64) << 1) | ((v3) as u64)) as u64) & 0xffffffffffu64);
    let v43: u64 = ((((((v42) as u64) << 1) | ((v3) as u64)) as u64) & 0x1ffffffffffu64);
    let v44: u64 = ((((((v43) as u64) << 1) | ((v3) as u64)) as u64) & 0x3ffffffffffu64);
    let v45: u64 = ((((((v44) as u64) << 1) | ((v3) as u64)) as u64) & 0x7ffffffffffu64);
    let v46: u64 = ((((((v45) as u64) << 1) | ((v3) as u64)) as u64) & 0xfffffffffffu64);
    let v47: u64 = ((((((v46) as u64) << 1) | ((v3) as u64)) as u64) & 0x1fffffffffffu64);
    let v48: u64 = ((((((v47) as u64) << 1) | ((v3) as u64)) as u64) & 0x3fffffffffffu64);
    let v49: u64 = ((((((v48) as u64) << 1) | ((v3) as u64)) as u64) & 0x7fffffffffffu64);
    let v50: u64 = ((((((v49) as u64) << 1) | ((v3) as u64)) as u64) & 0xffffffffffffu64);
    let v51: u64 = (((((v50) as u64) << 16) | ((v2) as u64)) as u64);
    ((v51) as u64)
}
