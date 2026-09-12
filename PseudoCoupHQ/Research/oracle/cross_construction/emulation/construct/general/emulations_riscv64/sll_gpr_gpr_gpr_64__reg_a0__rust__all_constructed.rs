#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of sll_gpr_gpr_gpr_64__reg_a0__rust__all_constructed.
//   v0 << Concat(0, Extract(5, 0, v1))
#[no_mangle]
pub extern "C" fn emu_sll_gpr_gpr_gpr_64__reg_a0__rust__all_constructed(a: u64, b: u8) -> u64
{
    let v0: u32 = (((((b as u32)) >> 0) as u32) & 0x3fu32);
    let v1: u32 = v0;
    let v2: u64 = 0x0u64;
    let v3: u64 = (((((v2) as u64) << 6) | ((v1) as u64)) as u64);
    let v4: u32 = (((((v3) as u64) >> 5) as u32) & 0x1u32);
    let v5: bool = (((0x1u32) as u32) == ((v4) as u32));
    let v6: u64 = (if (v5) { ((0xffffffffffffffffu64) as u64) } else { ((0x0u64) as u64) });
    let v7: u64 = ((!((v6) as u64)) as u64);
    let v8: u32 = (((((v3) as u64) >> 4) as u32) & 0x1u32);
    let v9: bool = (((0x1u32) as u32) == ((v8) as u32));
    let v10: u64 = (if (v9) { ((0xffffffffffffffffu64) as u64) } else { ((0x0u64) as u64) });
    let v11: u64 = ((!((v10) as u64)) as u64);
    let v12: u32 = (((((v3) as u64) >> 3) as u32) & 0x1u32);
    let v13: bool = (((0x1u32) as u32) == ((v12) as u32));
    let v14: u64 = (if (v13) { ((0xffffffffffffffffu64) as u64) } else { ((0x0u64) as u64) });
    let v15: u64 = ((!((v14) as u64)) as u64);
    let v16: u32 = (((((v3) as u64) >> 2) as u32) & 0x1u32);
    let v17: bool = (((0x1u32) as u32) == ((v16) as u32));
    let v18: u64 = (if (v17) { ((0xffffffffffffffffu64) as u64) } else { ((0x0u64) as u64) });
    let v19: u64 = ((!((v18) as u64)) as u64);
    let v20: u32 = (((((v3) as u64) >> 1) as u32) & 0x1u32);
    let v21: bool = (((0x1u32) as u32) == ((v20) as u32));
    let v22: u64 = (if (v21) { ((0xffffffffffffffffu64) as u64) } else { ((0x0u64) as u64) });
    let v23: u64 = ((!((v22) as u64)) as u64);
    let v24: u32 = (((((v3) as u64) >> 0) as u32) & 0x1u32);
    let v25: bool = (((0x1u32) as u32) == ((v24) as u32));
    let v26: u64 = (if (v25) { ((0xffffffffffffffffu64) as u64) } else { ((0x0u64) as u64) });
    let v27: u64 = ((!((v26) as u64)) as u64);
    let v28: u64 = (((((a as u64)) as u64) & ((v27) as u64)) as u64);
    let v29: u64 = (((((a as u64)) as u64).wrapping_shl((((0x1u64) as u64) as u32))) as u64);
    let v30: u64 = ((((v29) as u64) & ((v26) as u64)) as u64);
    let v31: u64 = ((((v30) as u64) | ((v28) as u64)) as u64);
    let v32: u64 = ((((v31) as u64) & ((v23) as u64)) as u64);
    let v33: u64 = ((((v31) as u64).wrapping_shl((((0x2u64) as u64) as u32))) as u64);
    let v34: u64 = ((((v33) as u64) & ((v22) as u64)) as u64);
    let v35: u64 = ((((v34) as u64) | ((v32) as u64)) as u64);
    let v36: u64 = ((((v35) as u64) & ((v19) as u64)) as u64);
    let v37: u64 = ((((v35) as u64).wrapping_shl((((0x4u64) as u64) as u32))) as u64);
    let v38: u64 = ((((v37) as u64) & ((v18) as u64)) as u64);
    let v39: u64 = ((((v38) as u64) | ((v36) as u64)) as u64);
    let v40: u64 = ((((v39) as u64) & ((v15) as u64)) as u64);
    let v41: u64 = ((((v39) as u64).wrapping_shl((((0x8u64) as u64) as u32))) as u64);
    let v42: u64 = ((((v41) as u64) & ((v14) as u64)) as u64);
    let v43: u64 = ((((v42) as u64) | ((v40) as u64)) as u64);
    let v44: u64 = ((((v43) as u64) & ((v11) as u64)) as u64);
    let v45: u64 = ((((v43) as u64).wrapping_shl((((0x10u64) as u64) as u32))) as u64);
    let v46: u64 = ((((v45) as u64) & ((v10) as u64)) as u64);
    let v47: u64 = ((((v46) as u64) | ((v44) as u64)) as u64);
    let v48: u64 = ((((v47) as u64) & ((v7) as u64)) as u64);
    let v49: u64 = ((((v47) as u64).wrapping_shl((((0x20u64) as u64) as u32))) as u64);
    let v50: u64 = ((((v49) as u64) & ((v6) as u64)) as u64);
    let v51: u64 = ((((v50) as u64) | ((v48) as u64)) as u64);
    let v52: u64 = ((0x1u32) as u64);
    let v53: u64 = ((!((0x40u64) as u64)) as u64);
    let v54: u64 = ((((v3) as u64) ^ ((v53) as u64)) as u64);
    let v55: u64 = ((((v54) as u64) & ((v52) as u64)) as u64);
    let v56: u64 = ((((v3) as u64) & ((v53) as u64)) as u64);
    let v57: u64 = ((((v56) as u64) | ((v55) as u64)) as u64);
    let v58: u64 = ((((v57) as u64).wrapping_shl((((0x1u64) as u64) as u32))) as u64);
    let v59: u64 = ((((v54) as u64) & ((v58) as u64)) as u64);
    let v60: u64 = ((((v57) as u64) | ((v59) as u64)) as u64);
    let v61: u64 = ((((v60) as u64).wrapping_shl((((0x2u64) as u64) as u32))) as u64);
    let v62: u64 = ((((v54) as u64).wrapping_shl((((0x1u64) as u64) as u32))) as u64);
    let v63: u64 = ((((v54) as u64) & ((v62) as u64)) as u64);
    let v64: u64 = ((((v63) as u64) & ((v61) as u64)) as u64);
    let v65: u64 = ((((v60) as u64) | ((v64) as u64)) as u64);
    let v66: u64 = ((((v65) as u64).wrapping_shl((((0x4u64) as u64) as u32))) as u64);
    let v67: u64 = ((((v63) as u64).wrapping_shl((((0x2u64) as u64) as u32))) as u64);
    let v68: u64 = ((((v63) as u64) & ((v67) as u64)) as u64);
    let v69: u64 = ((((v68) as u64) & ((v66) as u64)) as u64);
    let v70: u64 = ((((v65) as u64) | ((v69) as u64)) as u64);
    let v71: u64 = ((((v70) as u64).wrapping_shl((((0x8u64) as u64) as u32))) as u64);
    let v72: u64 = ((((v68) as u64).wrapping_shl((((0x4u64) as u64) as u32))) as u64);
    let v73: u64 = ((((v68) as u64) & ((v72) as u64)) as u64);
    let v74: u64 = ((((v73) as u64) & ((v71) as u64)) as u64);
    let v75: u64 = ((((v70) as u64) | ((v74) as u64)) as u64);
    let v76: u64 = ((((v75) as u64).wrapping_shl((((0x10u64) as u64) as u32))) as u64);
    let v77: u64 = ((((v73) as u64).wrapping_shl((((0x8u64) as u64) as u32))) as u64);
    let v78: u64 = ((((v73) as u64) & ((v77) as u64)) as u64);
    let v79: u64 = ((((v78) as u64) & ((v76) as u64)) as u64);
    let v80: u64 = ((((v75) as u64) | ((v79) as u64)) as u64);
    let v81: u64 = ((((v80) as u64).wrapping_shl((((0x20u64) as u64) as u32))) as u64);
    let v82: u64 = ((((v78) as u64).wrapping_shl((((0x10u64) as u64) as u32))) as u64);
    let v83: u64 = ((((v78) as u64) & ((v82) as u64)) as u64);
    let v84: u64 = ((((v83) as u64) & ((v81) as u64)) as u64);
    let v85: u64 = ((((v80) as u64) | ((v84) as u64)) as u64);
    let v86: u32 = (((((v85) as u64) >> 63) as u32) & 0x1u32);
    let v87: bool = (((0x0u32) as u32) == ((v86) as u32));
    let v88: bool = (!(v87));
    let v89: u64 = (if (v88) { ((0x0u64) as u64) } else { ((v51) as u64) });
    ((v89) as u64)
}
