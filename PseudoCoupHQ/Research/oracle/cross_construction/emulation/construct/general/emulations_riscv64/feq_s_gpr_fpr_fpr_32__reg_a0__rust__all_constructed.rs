#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of feq_s_gpr_fpr_fpr_32__reg_a0__rust__all_constructed.
//   If(fpEQ(fpToFP(Extract(31, 0, v0)), fpToFP(Extract(31, 0, v1))), 1, 0)
#[no_mangle]
pub extern "C" fn emu_feq_s_gpr_fpr_fpr_32__reg_a0__rust__all_constructed(a: u32, b: u32) -> u64
{
    let v0: u32 = (b as u32);
    let v1: u32 = (a as u32);
    let v2: u32 = ((((v1) as u32) ^ ((v0) as u32)) as u32);
    let v3: u32 = ((((v2) as u32).wrapping_shr((((0x1u32) as u32) as u32))) as u32);
    let v4: u32 = ((((v2) as u32) | ((v3) as u32)) as u32);
    let v5: u32 = ((((v4) as u32).wrapping_shr((((0x2u32) as u32) as u32))) as u32);
    let v6: u32 = ((((v4) as u32) | ((v5) as u32)) as u32);
    let v7: u32 = ((((v6) as u32).wrapping_shr((((0x4u32) as u32) as u32))) as u32);
    let v8: u32 = ((((v6) as u32) | ((v7) as u32)) as u32);
    let v9: u32 = ((((v8) as u32).wrapping_shr((((0x8u32) as u32) as u32))) as u32);
    let v10: u32 = ((((v8) as u32) | ((v9) as u32)) as u32);
    let v11: u32 = ((((v10) as u32).wrapping_shr((((0x10u32) as u32) as u32))) as u32);
    let v12: u32 = ((((v10) as u32) | ((v11) as u32)) as u32);
    let v13: u32 = (((((v12) as u32) >> 0) as u32) & 0x1u32);
    let v14: bool = (((0x1u32) as u32) == ((v13) as u32));
    let v15: bool = (!(v14));
    let v16: u32 = (((((v0) as u32) >> 0) as u32) & 0x7fffffu32);
    let v17: u32 = (((((v16) as u32).wrapping_shr((((0x1u32) as u32) as u32))) as u32) & 0x7fffffu32);
    let v18: u32 = (((((v16) as u32) | ((v17) as u32)) as u32) & 0x7fffffu32);
    let v19: u32 = (((((v18) as u32).wrapping_shr((((0x2u32) as u32) as u32))) as u32) & 0x7fffffu32);
    let v20: u32 = (((((v18) as u32) | ((v19) as u32)) as u32) & 0x7fffffu32);
    let v21: u32 = (((((v20) as u32).wrapping_shr((((0x4u32) as u32) as u32))) as u32) & 0x7fffffu32);
    let v22: u32 = (((((v20) as u32) | ((v21) as u32)) as u32) & 0x7fffffu32);
    let v23: u32 = (((((v22) as u32).wrapping_shr((((0x8u32) as u32) as u32))) as u32) & 0x7fffffu32);
    let v24: u32 = (((((v22) as u32) | ((v23) as u32)) as u32) & 0x7fffffu32);
    let v25: u32 = (((((v24) as u32).wrapping_shr((((0x10u32) as u32) as u32))) as u32) & 0x7fffffu32);
    let v26: u32 = (((((v24) as u32) | ((v25) as u32)) as u32) & 0x7fffffu32);
    let v27: u32 = (((((v26) as u32) >> 0) as u32) & 0x1u32);
    let v28: bool = (((0x1u32) as u32) == ((v27) as u32));
    let v29: bool = (!(v28));
    let v30: u32 = (((((v0) as u32) >> 23) as u32) & 0xffu32);
    let v31: u32 = (((((v30) as u32).wrapping_shr((((0x1u32) as u32) as u32))) as u32) & 0xffu32);
    let v32: u32 = (((((v30) as u32) | ((v31) as u32)) as u32) & 0xffu32);
    let v33: u32 = (((((v32) as u32).wrapping_shr((((0x2u32) as u32) as u32))) as u32) & 0xffu32);
    let v34: u32 = (((((v32) as u32) | ((v33) as u32)) as u32) & 0xffu32);
    let v35: u32 = (((((v34) as u32).wrapping_shr((((0x4u32) as u32) as u32))) as u32) & 0xffu32);
    let v36: u32 = (((((v34) as u32) | ((v35) as u32)) as u32) & 0xffu32);
    let v37: u32 = (((((v36) as u32) >> 0) as u32) & 0x1u32);
    let v38: bool = (((0x1u32) as u32) == ((v37) as u32));
    let v39: bool = (!(v38));
    let v40: bool = ((v39) && (v29));
    let v41: u32 = (((((v1) as u32) >> 0) as u32) & 0x7fffffu32);
    let v42: u32 = (((((v41) as u32).wrapping_shr((((0x1u32) as u32) as u32))) as u32) & 0x7fffffu32);
    let v43: u32 = (((((v41) as u32) | ((v42) as u32)) as u32) & 0x7fffffu32);
    let v44: u32 = (((((v43) as u32).wrapping_shr((((0x2u32) as u32) as u32))) as u32) & 0x7fffffu32);
    let v45: u32 = (((((v43) as u32) | ((v44) as u32)) as u32) & 0x7fffffu32);
    let v46: u32 = (((((v45) as u32).wrapping_shr((((0x4u32) as u32) as u32))) as u32) & 0x7fffffu32);
    let v47: u32 = (((((v45) as u32) | ((v46) as u32)) as u32) & 0x7fffffu32);
    let v48: u32 = (((((v47) as u32).wrapping_shr((((0x8u32) as u32) as u32))) as u32) & 0x7fffffu32);
    let v49: u32 = (((((v47) as u32) | ((v48) as u32)) as u32) & 0x7fffffu32);
    let v50: u32 = (((((v49) as u32).wrapping_shr((((0x10u32) as u32) as u32))) as u32) & 0x7fffffu32);
    let v51: u32 = (((((v49) as u32) | ((v50) as u32)) as u32) & 0x7fffffu32);
    let v52: u32 = (((((v51) as u32) >> 0) as u32) & 0x1u32);
    let v53: bool = (((0x1u32) as u32) == ((v52) as u32));
    let v54: bool = (!(v53));
    let v55: u32 = (((((v1) as u32) >> 23) as u32) & 0xffu32);
    let v56: u32 = (((((v55) as u32).wrapping_shr((((0x1u32) as u32) as u32))) as u32) & 0xffu32);
    let v57: u32 = (((((v55) as u32) | ((v56) as u32)) as u32) & 0xffu32);
    let v58: u32 = (((((v57) as u32).wrapping_shr((((0x2u32) as u32) as u32))) as u32) & 0xffu32);
    let v59: u32 = (((((v57) as u32) | ((v58) as u32)) as u32) & 0xffu32);
    let v60: u32 = (((((v59) as u32).wrapping_shr((((0x4u32) as u32) as u32))) as u32) & 0xffu32);
    let v61: u32 = (((((v59) as u32) | ((v60) as u32)) as u32) & 0xffu32);
    let v62: u32 = (((((v61) as u32) >> 0) as u32) & 0x1u32);
    let v63: bool = (((0x1u32) as u32) == ((v62) as u32));
    let v64: bool = (!(v63));
    let v65: bool = ((v64) && (v54));
    let v66: bool = ((v65) && (v40));
    let v67: bool = ((v66) || (v15));
    let v68: bool = (!(v29));
    let v69: u32 = (((((v30) as u32) ^ ((0xffu32) as u32)) as u32) & 0xffu32);
    let v70: u32 = (((((v69) as u32).wrapping_shr((((0x1u32) as u32) as u32))) as u32) & 0xffu32);
    let v71: u32 = (((((v69) as u32) | ((v70) as u32)) as u32) & 0xffu32);
    let v72: u32 = (((((v71) as u32).wrapping_shr((((0x2u32) as u32) as u32))) as u32) & 0xffu32);
    let v73: u32 = (((((v71) as u32) | ((v72) as u32)) as u32) & 0xffu32);
    let v74: u32 = (((((v73) as u32).wrapping_shr((((0x4u32) as u32) as u32))) as u32) & 0xffu32);
    let v75: u32 = (((((v73) as u32) | ((v74) as u32)) as u32) & 0xffu32);
    let v76: u32 = (((((v75) as u32) >> 0) as u32) & 0x1u32);
    let v77: bool = (((0x1u32) as u32) == ((v76) as u32));
    let v78: bool = (!(v77));
    let v79: bool = ((v78) && (v68));
    let v80: bool = (!(v79));
    let v81: bool = (!(v54));
    let v82: u32 = (((((v55) as u32) ^ ((0xffu32) as u32)) as u32) & 0xffu32);
    let v83: u32 = (((((v82) as u32).wrapping_shr((((0x1u32) as u32) as u32))) as u32) & 0xffu32);
    let v84: u32 = (((((v82) as u32) | ((v83) as u32)) as u32) & 0xffu32);
    let v85: u32 = (((((v84) as u32).wrapping_shr((((0x2u32) as u32) as u32))) as u32) & 0xffu32);
    let v86: u32 = (((((v84) as u32) | ((v85) as u32)) as u32) & 0xffu32);
    let v87: u32 = (((((v86) as u32).wrapping_shr((((0x4u32) as u32) as u32))) as u32) & 0xffu32);
    let v88: u32 = (((((v86) as u32) | ((v87) as u32)) as u32) & 0xffu32);
    let v89: u32 = (((((v88) as u32) >> 0) as u32) & 0x1u32);
    let v90: bool = (((0x1u32) as u32) == ((v89) as u32));
    let v91: bool = (!(v90));
    let v92: bool = ((v91) && (v81));
    let v93: bool = (!(v92));
    let v94: bool = ((v93) && (v80));
    let v95: bool = ((v94) && (v67));
    let v96: u64 = (if (v95) { ((0x1u64) as u64) } else { ((0x0u64) as u64) });
    ((v96) as u64)
}
