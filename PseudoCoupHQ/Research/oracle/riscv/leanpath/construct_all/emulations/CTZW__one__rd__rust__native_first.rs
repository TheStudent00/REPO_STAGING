#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of CTZW__one__rd__rust__native_first.
//   
#[no_mangle]
pub extern "C" fn emu_CTZW__one__rd__rust__native_first(a: u32) -> u64
{
    let v0: u32 = (((((a as u32)) >> 31) as u32) & 0x1u32);
    let v1: bool = (((v0) as u32) == ((0x1u32) as u32));
    let v2: u32 = (if (v1) { ((0x1fu32) as u32) } else { ((0x20u32) as u32) });
    let v3: u32 = (((((a as u32)) >> 30) as u32) & 0x1u32);
    let v4: bool = (((v3) as u32) == ((0x1u32) as u32));
    let v5: u32 = (if (v4) { ((0x1eu32) as u32) } else { ((v2) as u32) });
    let v6: u32 = (((((a as u32)) >> 29) as u32) & 0x1u32);
    let v7: bool = (((v6) as u32) == ((0x1u32) as u32));
    let v8: u32 = (if (v7) { ((0x1du32) as u32) } else { ((v5) as u32) });
    let v9: u32 = (((((a as u32)) >> 28) as u32) & 0x1u32);
    let v10: bool = (((v9) as u32) == ((0x1u32) as u32));
    let v11: u32 = (if (v10) { ((0x1cu32) as u32) } else { ((v8) as u32) });
    let v12: u32 = (((((a as u32)) >> 27) as u32) & 0x1u32);
    let v13: bool = (((v12) as u32) == ((0x1u32) as u32));
    let v14: u32 = (if (v13) { ((0x1bu32) as u32) } else { ((v11) as u32) });
    let v15: u32 = (((((a as u32)) >> 26) as u32) & 0x1u32);
    let v16: bool = (((v15) as u32) == ((0x1u32) as u32));
    let v17: u32 = (if (v16) { ((0x1au32) as u32) } else { ((v14) as u32) });
    let v18: u32 = (((((a as u32)) >> 25) as u32) & 0x1u32);
    let v19: bool = (((v18) as u32) == ((0x1u32) as u32));
    let v20: u32 = (if (v19) { ((0x19u32) as u32) } else { ((v17) as u32) });
    let v21: u32 = (((((a as u32)) >> 24) as u32) & 0x1u32);
    let v22: bool = (((v21) as u32) == ((0x1u32) as u32));
    let v23: u32 = (if (v22) { ((0x18u32) as u32) } else { ((v20) as u32) });
    let v24: u32 = (((((a as u32)) >> 23) as u32) & 0x1u32);
    let v25: bool = (((v24) as u32) == ((0x1u32) as u32));
    let v26: u32 = (if (v25) { ((0x17u32) as u32) } else { ((v23) as u32) });
    let v27: u32 = (((((a as u32)) >> 22) as u32) & 0x1u32);
    let v28: bool = (((v27) as u32) == ((0x1u32) as u32));
    let v29: u32 = (if (v28) { ((0x16u32) as u32) } else { ((v26) as u32) });
    let v30: u32 = (((((a as u32)) >> 21) as u32) & 0x1u32);
    let v31: bool = (((v30) as u32) == ((0x1u32) as u32));
    let v32: u32 = (if (v31) { ((0x15u32) as u32) } else { ((v29) as u32) });
    let v33: u32 = (((((a as u32)) >> 20) as u32) & 0x1u32);
    let v34: bool = (((v33) as u32) == ((0x1u32) as u32));
    let v35: u32 = (if (v34) { ((0x14u32) as u32) } else { ((v32) as u32) });
    let v36: u32 = (((((a as u32)) >> 19) as u32) & 0x1u32);
    let v37: bool = (((v36) as u32) == ((0x1u32) as u32));
    let v38: u32 = (if (v37) { ((0x13u32) as u32) } else { ((v35) as u32) });
    let v39: u32 = (((((a as u32)) >> 18) as u32) & 0x1u32);
    let v40: bool = (((v39) as u32) == ((0x1u32) as u32));
    let v41: u32 = (if (v40) { ((0x12u32) as u32) } else { ((v38) as u32) });
    let v42: u32 = (((((a as u32)) >> 17) as u32) & 0x1u32);
    let v43: bool = (((v42) as u32) == ((0x1u32) as u32));
    let v44: u32 = (if (v43) { ((0x11u32) as u32) } else { ((v41) as u32) });
    let v45: u32 = (((((a as u32)) >> 16) as u32) & 0x1u32);
    let v46: bool = (((v45) as u32) == ((0x1u32) as u32));
    let v47: u32 = (if (v46) { ((0x10u32) as u32) } else { ((v44) as u32) });
    let v48: u32 = (((((a as u32)) >> 15) as u32) & 0x1u32);
    let v49: bool = (((v48) as u32) == ((0x1u32) as u32));
    let v50: u32 = (if (v49) { ((0xfu32) as u32) } else { ((v47) as u32) });
    let v51: u32 = (((((a as u32)) >> 14) as u32) & 0x1u32);
    let v52: bool = (((v51) as u32) == ((0x1u32) as u32));
    let v53: u32 = (if (v52) { ((0xeu32) as u32) } else { ((v50) as u32) });
    let v54: u32 = (((((a as u32)) >> 13) as u32) & 0x1u32);
    let v55: bool = (((v54) as u32) == ((0x1u32) as u32));
    let v56: u32 = (if (v55) { ((0xdu32) as u32) } else { ((v53) as u32) });
    let v57: u32 = (((((a as u32)) >> 12) as u32) & 0x1u32);
    let v58: bool = (((v57) as u32) == ((0x1u32) as u32));
    let v59: u32 = (if (v58) { ((0xcu32) as u32) } else { ((v56) as u32) });
    let v60: u32 = (((((a as u32)) >> 11) as u32) & 0x1u32);
    let v61: bool = (((v60) as u32) == ((0x1u32) as u32));
    let v62: u32 = (if (v61) { ((0xbu32) as u32) } else { ((v59) as u32) });
    let v63: u32 = (((((a as u32)) >> 10) as u32) & 0x1u32);
    let v64: bool = (((v63) as u32) == ((0x1u32) as u32));
    let v65: u32 = (if (v64) { ((0xau32) as u32) } else { ((v62) as u32) });
    let v66: u32 = (((((a as u32)) >> 9) as u32) & 0x1u32);
    let v67: bool = (((v66) as u32) == ((0x1u32) as u32));
    let v68: u32 = (if (v67) { ((0x9u32) as u32) } else { ((v65) as u32) });
    let v69: u32 = (((((a as u32)) >> 8) as u32) & 0x1u32);
    let v70: bool = (((v69) as u32) == ((0x1u32) as u32));
    let v71: u32 = (if (v70) { ((0x8u32) as u32) } else { ((v68) as u32) });
    let v72: u32 = (((((a as u32)) >> 7) as u32) & 0x1u32);
    let v73: bool = (((v72) as u32) == ((0x1u32) as u32));
    let v74: u32 = (if (v73) { ((0x7u32) as u32) } else { ((v71) as u32) });
    let v75: u32 = (((((a as u32)) >> 6) as u32) & 0x1u32);
    let v76: bool = (((v75) as u32) == ((0x1u32) as u32));
    let v77: u32 = (if (v76) { ((0x6u32) as u32) } else { ((v74) as u32) });
    let v78: u32 = (((((a as u32)) >> 5) as u32) & 0x1u32);
    let v79: bool = (((v78) as u32) == ((0x1u32) as u32));
    let v80: u32 = (if (v79) { ((0x5u32) as u32) } else { ((v77) as u32) });
    let v81: u32 = (((((a as u32)) >> 4) as u32) & 0x1u32);
    let v82: bool = (((v81) as u32) == ((0x1u32) as u32));
    let v83: u32 = (if (v82) { ((0x4u32) as u32) } else { ((v80) as u32) });
    let v84: u32 = (((((a as u32)) >> 3) as u32) & 0x1u32);
    let v85: bool = (((v84) as u32) == ((0x1u32) as u32));
    let v86: u32 = (if (v85) { ((0x3u32) as u32) } else { ((v83) as u32) });
    let v87: u32 = (((((a as u32)) >> 2) as u32) & 0x1u32);
    let v88: bool = (((v87) as u32) == ((0x1u32) as u32));
    let v89: u32 = (if (v88) { ((0x2u32) as u32) } else { ((v86) as u32) });
    let v90: u32 = (((((a as u32)) >> 1) as u32) & 0x1u32);
    let v91: bool = (((v90) as u32) == ((0x1u32) as u32));
    let v92: u32 = (if (v91) { ((0x1u32) as u32) } else { ((v89) as u32) });
    let v93: u32 = (((((a as u32)) >> 0) as u32) & 0x1u32);
    let v94: bool = (((v93) as u32) == ((0x1u32) as u32));
    let v95: u32 = (if (v94) { ((0x0u32) as u32) } else { ((v92) as u32) });
    let v96: u64 = (((((0x0u32) as u64) << 32) | ((v95) as u64)) as u64);
    ((v96) as u64)
}
