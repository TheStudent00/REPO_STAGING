#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of BREV8__one__rd__rust__native_first.
//   
#[no_mangle]
pub extern "C" fn emu_BREV8__one__rd__rust__native_first(a: u64) -> u64
{
    let v0: u32 = (((((a as u64)) >> 7) as u32) & 0x1u32);
    let v1: u32 = (((((a as u64)) >> 6) as u32) & 0x1u32);
    let v2: u32 = (((((a as u64)) >> 5) as u32) & 0x1u32);
    let v3: u32 = (((((a as u64)) >> 4) as u32) & 0x1u32);
    let v4: u32 = (((((a as u64)) >> 3) as u32) & 0x1u32);
    let v5: u32 = (((((a as u64)) >> 2) as u32) & 0x1u32);
    let v6: u32 = (((((a as u64)) >> 1) as u32) & 0x1u32);
    let v7: u32 = (((((a as u64)) >> 0) as u32) & 0x1u32);
    let v8: u32 = (((((a as u64)) >> 15) as u32) & 0x1u32);
    let v9: u32 = (((((a as u64)) >> 14) as u32) & 0x1u32);
    let v10: u32 = (((((a as u64)) >> 13) as u32) & 0x1u32);
    let v11: u32 = (((((a as u64)) >> 12) as u32) & 0x1u32);
    let v12: u32 = (((((a as u64)) >> 11) as u32) & 0x1u32);
    let v13: u32 = (((((a as u64)) >> 10) as u32) & 0x1u32);
    let v14: u32 = (((((a as u64)) >> 9) as u32) & 0x1u32);
    let v15: u32 = (((((a as u64)) >> 8) as u32) & 0x1u32);
    let v16: u32 = (((((a as u64)) >> 23) as u32) & 0x1u32);
    let v17: u32 = (((((a as u64)) >> 22) as u32) & 0x1u32);
    let v18: u32 = (((((a as u64)) >> 21) as u32) & 0x1u32);
    let v19: u32 = (((((a as u64)) >> 20) as u32) & 0x1u32);
    let v20: u32 = (((((a as u64)) >> 19) as u32) & 0x1u32);
    let v21: u32 = (((((a as u64)) >> 18) as u32) & 0x1u32);
    let v22: u32 = (((((a as u64)) >> 17) as u32) & 0x1u32);
    let v23: u32 = (((((a as u64)) >> 16) as u32) & 0x1u32);
    let v24: u32 = (((((a as u64)) >> 31) as u32) & 0x1u32);
    let v25: u32 = (((((a as u64)) >> 30) as u32) & 0x1u32);
    let v26: u32 = (((((a as u64)) >> 29) as u32) & 0x1u32);
    let v27: u32 = (((((a as u64)) >> 28) as u32) & 0x1u32);
    let v28: u32 = (((((a as u64)) >> 27) as u32) & 0x1u32);
    let v29: u32 = (((((a as u64)) >> 26) as u32) & 0x1u32);
    let v30: u32 = (((((a as u64)) >> 25) as u32) & 0x1u32);
    let v31: u32 = (((((a as u64)) >> 24) as u32) & 0x1u32);
    let v32: u32 = (((((a as u64)) >> 39) as u32) & 0x1u32);
    let v33: u32 = (((((a as u64)) >> 38) as u32) & 0x1u32);
    let v34: u32 = (((((a as u64)) >> 37) as u32) & 0x1u32);
    let v35: u32 = (((((a as u64)) >> 36) as u32) & 0x1u32);
    let v36: u32 = (((((a as u64)) >> 35) as u32) & 0x1u32);
    let v37: u32 = (((((a as u64)) >> 34) as u32) & 0x1u32);
    let v38: u32 = (((((a as u64)) >> 33) as u32) & 0x1u32);
    let v39: u32 = (((((a as u64)) >> 32) as u32) & 0x1u32);
    let v40: u32 = (((((a as u64)) >> 47) as u32) & 0x1u32);
    let v41: u32 = (((((a as u64)) >> 46) as u32) & 0x1u32);
    let v42: u32 = (((((a as u64)) >> 45) as u32) & 0x1u32);
    let v43: u32 = (((((a as u64)) >> 44) as u32) & 0x1u32);
    let v44: u32 = (((((a as u64)) >> 43) as u32) & 0x1u32);
    let v45: u32 = (((((a as u64)) >> 42) as u32) & 0x1u32);
    let v46: u32 = (((((a as u64)) >> 41) as u32) & 0x1u32);
    let v47: u32 = (((((a as u64)) >> 40) as u32) & 0x1u32);
    let v48: u32 = (((((a as u64)) >> 55) as u32) & 0x1u32);
    let v49: u32 = (((((a as u64)) >> 54) as u32) & 0x1u32);
    let v50: u32 = (((((a as u64)) >> 53) as u32) & 0x1u32);
    let v51: u32 = (((((a as u64)) >> 52) as u32) & 0x1u32);
    let v52: u32 = (((((a as u64)) >> 51) as u32) & 0x1u32);
    let v53: u32 = (((((a as u64)) >> 50) as u32) & 0x1u32);
    let v54: u32 = (((((a as u64)) >> 49) as u32) & 0x1u32);
    let v55: u32 = (((((a as u64)) >> 48) as u32) & 0x1u32);
    let v56: u32 = (((((a as u64)) >> 63) as u32) & 0x1u32);
    let v57: u32 = (((((a as u64)) >> 62) as u32) & 0x1u32);
    let v58: u32 = (((((a as u64)) >> 61) as u32) & 0x1u32);
    let v59: u32 = (((((a as u64)) >> 60) as u32) & 0x1u32);
    let v60: u32 = (((((a as u64)) >> 59) as u32) & 0x1u32);
    let v61: u32 = (((((a as u64)) >> 58) as u32) & 0x1u32);
    let v62: u32 = (((((a as u64)) >> 57) as u32) & 0x1u32);
    let v63: u32 = (((((a as u64)) >> 56) as u32) & 0x1u32);
    let v64: u64 = (((((v63) as u64) << 63) | (((v62) as u64) << 62) | (((v61) as u64) << 61) | (((v60) as u64) << 60) | (((v59) as u64) << 59) | (((v58) as u64) << 58) | (((v57) as u64) << 57) | (((v56) as u64) << 56) | (((v55) as u64) << 55) | (((v54) as u64) << 54) | (((v53) as u64) << 53) | (((v52) as u64) << 52) | (((v51) as u64) << 51) | (((v50) as u64) << 50) | (((v49) as u64) << 49) | (((v48) as u64) << 48) | (((v47) as u64) << 47) | (((v46) as u64) << 46) | (((v45) as u64) << 45) | (((v44) as u64) << 44) | (((v43) as u64) << 43) | (((v42) as u64) << 42) | (((v41) as u64) << 41) | (((v40) as u64) << 40) | (((v39) as u64) << 39) | (((v38) as u64) << 38) | (((v37) as u64) << 37) | (((v36) as u64) << 36) | (((v35) as u64) << 35) | (((v34) as u64) << 34) | (((v33) as u64) << 33) | (((v32) as u64) << 32) | (((v31) as u64) << 31) | (((v30) as u64) << 30) | (((v29) as u64) << 29) | (((v28) as u64) << 28) | (((v27) as u64) << 27) | (((v26) as u64) << 26) | (((v25) as u64) << 25) | (((v24) as u64) << 24) | (((v23) as u64) << 23) | (((v22) as u64) << 22) | (((v21) as u64) << 21) | (((v20) as u64) << 20) | (((v19) as u64) << 19) | (((v18) as u64) << 18) | (((v17) as u64) << 17) | (((v16) as u64) << 16) | (((v15) as u64) << 15) | (((v14) as u64) << 14) | (((v13) as u64) << 13) | (((v12) as u64) << 12) | (((v11) as u64) << 11) | (((v10) as u64) << 10) | (((v9) as u64) << 9) | (((v8) as u64) << 8) | (((v7) as u64) << 7) | (((v6) as u64) << 6) | (((v5) as u64) << 5) | (((v4) as u64) << 4) | (((v3) as u64) << 3) | (((v2) as u64) << 2) | (((v1) as u64) << 1) | ((v0) as u64)) as u64);
    ((v64) as u64)
}
