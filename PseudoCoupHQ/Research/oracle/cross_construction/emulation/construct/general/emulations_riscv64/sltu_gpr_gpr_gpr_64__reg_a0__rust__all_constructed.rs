#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of sltu_gpr_gpr_gpr_64__reg_a0__rust__all_constructed.
//   If(ULE(v0, v1), 0, 1)
#[no_mangle]
pub extern "C" fn emu_sltu_gpr_gpr_gpr_64__reg_a0__rust__all_constructed(a: u64, b: u64) -> u64
{
    let v0: u64 = ((0x1u32) as u64);
    let v1: u64 = ((!(((b as u64)) as u64)) as u64);
    let v2: u64 = (((((a as u64)) as u64) ^ ((v1) as u64)) as u64);
    let v3: u64 = ((((v2) as u64) & ((v0) as u64)) as u64);
    let v4: u64 = (((((a as u64)) as u64) & ((v1) as u64)) as u64);
    let v5: u64 = ((((v4) as u64) | ((v3) as u64)) as u64);
    let v6: u64 = ((((v5) as u64).wrapping_shl((((0x1u64) as u64) as u32))) as u64);
    let v7: u64 = ((((v2) as u64) & ((v6) as u64)) as u64);
    let v8: u64 = ((((v5) as u64) | ((v7) as u64)) as u64);
    let v9: u64 = ((((v8) as u64).wrapping_shl((((0x2u64) as u64) as u32))) as u64);
    let v10: u64 = ((((v2) as u64).wrapping_shl((((0x1u64) as u64) as u32))) as u64);
    let v11: u64 = ((((v2) as u64) & ((v10) as u64)) as u64);
    let v12: u64 = ((((v11) as u64) & ((v9) as u64)) as u64);
    let v13: u64 = ((((v8) as u64) | ((v12) as u64)) as u64);
    let v14: u64 = ((((v13) as u64).wrapping_shl((((0x4u64) as u64) as u32))) as u64);
    let v15: u64 = ((((v11) as u64).wrapping_shl((((0x2u64) as u64) as u32))) as u64);
    let v16: u64 = ((((v11) as u64) & ((v15) as u64)) as u64);
    let v17: u64 = ((((v16) as u64) & ((v14) as u64)) as u64);
    let v18: u64 = ((((v13) as u64) | ((v17) as u64)) as u64);
    let v19: u64 = ((((v18) as u64).wrapping_shl((((0x8u64) as u64) as u32))) as u64);
    let v20: u64 = ((((v16) as u64).wrapping_shl((((0x4u64) as u64) as u32))) as u64);
    let v21: u64 = ((((v16) as u64) & ((v20) as u64)) as u64);
    let v22: u64 = ((((v21) as u64) & ((v19) as u64)) as u64);
    let v23: u64 = ((((v18) as u64) | ((v22) as u64)) as u64);
    let v24: u64 = ((((v23) as u64).wrapping_shl((((0x10u64) as u64) as u32))) as u64);
    let v25: u64 = ((((v21) as u64).wrapping_shl((((0x8u64) as u64) as u32))) as u64);
    let v26: u64 = ((((v21) as u64) & ((v25) as u64)) as u64);
    let v27: u64 = ((((v26) as u64) & ((v24) as u64)) as u64);
    let v28: u64 = ((((v23) as u64) | ((v27) as u64)) as u64);
    let v29: u64 = ((((v28) as u64).wrapping_shl((((0x20u64) as u64) as u32))) as u64);
    let v30: u64 = ((((v26) as u64).wrapping_shl((((0x10u64) as u64) as u32))) as u64);
    let v31: u64 = ((((v26) as u64) & ((v30) as u64)) as u64);
    let v32: u64 = ((((v31) as u64) & ((v29) as u64)) as u64);
    let v33: u64 = ((((v28) as u64) | ((v32) as u64)) as u64);
    let v34: u32 = (((((v33) as u64) >> 63) as u32) & 0x1u32);
    let v35: bool = (((0x0u32) as u32) == ((v34) as u32));
    let v36: bool = (!(v35));
    let v37: u64 = (if (v36) { ((0x0u64) as u64) } else { ((0x1u64) as u64) });
    ((v37) as u64)
}
