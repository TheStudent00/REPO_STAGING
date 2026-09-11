#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of seta_gpr_one_8__reg_rdi__rust__all_constructed.
//   Concat(Extract(63, 8, v2), If(And(ULE(Extract(7, 0, v0), Extract(7, 0, v1)), Not(Extract(7, 0, v0) == Extract(7, 0, v1))), 1, 0))
#[no_mangle]
pub extern "C" fn emu_seta_gpr_one_8__reg_rdi__rust__all_constructed(a: u8, b: u8, c: u64) -> u64
{
    let v0: u32 = (a as u32);
    let v1: u32 = (b as u32);
    let v2: u32 = (((((v1) as u32) ^ ((v0) as u32)) as u32) & 0xffu32);
    let v3: u32 = (((((v2) as u32).wrapping_shr((((0x1u32) as u32) as u32))) as u32) & 0xffu32);
    let v4: u32 = (((((v2) as u32) | ((v3) as u32)) as u32) & 0xffu32);
    let v5: u32 = (((((v4) as u32).wrapping_shr((((0x2u32) as u32) as u32))) as u32) & 0xffu32);
    let v6: u32 = (((((v4) as u32) | ((v5) as u32)) as u32) & 0xffu32);
    let v7: u32 = (((((v6) as u32).wrapping_shr((((0x4u32) as u32) as u32))) as u32) & 0xffu32);
    let v8: u32 = (((((v6) as u32) | ((v7) as u32)) as u32) & 0xffu32);
    let v9: u32 = (((((v8) as u32) >> 0) as u32) & 0x1u32);
    let v10: bool = (((0x1u32) as u32) == ((v9) as u32));
    let v11: bool = (!(v10));
    let v12: bool = (!(v11));
    let v13: u32 = ((0x1u32) as u32);
    let v14: u32 = (((!((v1) as u32)) as u32) & 0xffu32);
    let v15: u32 = (((((v0) as u32) ^ ((v14) as u32)) as u32) & 0xffu32);
    let v16: u32 = (((((v15) as u32) & ((v13) as u32)) as u32) & 0xffu32);
    let v17: u32 = (((((v0) as u32) & ((v14) as u32)) as u32) & 0xffu32);
    let v18: u32 = (((((v17) as u32) | ((v16) as u32)) as u32) & 0xffu32);
    let v19: u32 = (((((v18) as u32).wrapping_shl((((0x1u32) as u32) as u32))) as u32) & 0xffu32);
    let v20: u32 = (((((v15) as u32) & ((v19) as u32)) as u32) & 0xffu32);
    let v21: u32 = (((((v18) as u32) | ((v20) as u32)) as u32) & 0xffu32);
    let v22: u32 = (((((v21) as u32).wrapping_shl((((0x2u32) as u32) as u32))) as u32) & 0xffu32);
    let v23: u32 = (((((v15) as u32).wrapping_shl((((0x1u32) as u32) as u32))) as u32) & 0xffu32);
    let v24: u32 = (((((v15) as u32) & ((v23) as u32)) as u32) & 0xffu32);
    let v25: u32 = (((((v24) as u32) & ((v22) as u32)) as u32) & 0xffu32);
    let v26: u32 = (((((v21) as u32) | ((v25) as u32)) as u32) & 0xffu32);
    let v27: u32 = (((((v26) as u32).wrapping_shl((((0x4u32) as u32) as u32))) as u32) & 0xffu32);
    let v28: u32 = (((((v24) as u32).wrapping_shl((((0x2u32) as u32) as u32))) as u32) & 0xffu32);
    let v29: u32 = (((((v24) as u32) & ((v28) as u32)) as u32) & 0xffu32);
    let v30: u32 = (((((v29) as u32) & ((v27) as u32)) as u32) & 0xffu32);
    let v31: u32 = (((((v26) as u32) | ((v30) as u32)) as u32) & 0xffu32);
    let v32: u32 = (((((v31) as u32) >> 7) as u32) & 0x1u32);
    let v33: bool = (((0x0u32) as u32) == ((v32) as u32));
    let v34: bool = (!(v33));
    let v35: bool = ((v34) && (v12));
    let v36: u32 = (if (v35) { ((0x1u32) as u32) } else { ((0x0u32) as u32) });
    let v37: u64 = (((((c as u64)) >> 8) as u64) & 0xffffffffffffffu64);
    let v38: u32 = v36;
    let v39: u64 = v37;
    let v40: u64 = (((((v39) as u64) << 8) | ((v38) as u64)) as u64);
    ((v40) as u64)
}
