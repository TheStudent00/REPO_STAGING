#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of setae_gpr_one_8__reg_rdi__rust__all_constructed.
//   Concat(Extract(63, 8, v0), If(ULE(Extract(7, 0, v1), Extract(7, 0, v2)), 1, 0))
#[no_mangle]
pub extern "C" fn emu_setae_gpr_one_8__reg_rdi__rust__all_constructed(a: u8, b: u8, c: u64) -> u64
{
    let v0: u32 = (a as u32);
    let v1: u32 = (b as u32);
    let v2: u32 = ((0x1u32) as u32);
    let v3: u32 = (((!((v1) as u32)) as u32) & 0xffu32);
    let v4: u32 = (((((v0) as u32) ^ ((v3) as u32)) as u32) & 0xffu32);
    let v5: u32 = (((((v4) as u32) & ((v2) as u32)) as u32) & 0xffu32);
    let v6: u32 = (((((v0) as u32) & ((v3) as u32)) as u32) & 0xffu32);
    let v7: u32 = (((((v6) as u32) | ((v5) as u32)) as u32) & 0xffu32);
    let v8: u32 = (((((v7) as u32).wrapping_shl((((0x1u32) as u32) as u32))) as u32) & 0xffu32);
    let v9: u32 = (((((v4) as u32) & ((v8) as u32)) as u32) & 0xffu32);
    let v10: u32 = (((((v7) as u32) | ((v9) as u32)) as u32) & 0xffu32);
    let v11: u32 = (((((v10) as u32).wrapping_shl((((0x2u32) as u32) as u32))) as u32) & 0xffu32);
    let v12: u32 = (((((v4) as u32).wrapping_shl((((0x1u32) as u32) as u32))) as u32) & 0xffu32);
    let v13: u32 = (((((v4) as u32) & ((v12) as u32)) as u32) & 0xffu32);
    let v14: u32 = (((((v13) as u32) & ((v11) as u32)) as u32) & 0xffu32);
    let v15: u32 = (((((v10) as u32) | ((v14) as u32)) as u32) & 0xffu32);
    let v16: u32 = (((((v15) as u32).wrapping_shl((((0x4u32) as u32) as u32))) as u32) & 0xffu32);
    let v17: u32 = (((((v13) as u32).wrapping_shl((((0x2u32) as u32) as u32))) as u32) & 0xffu32);
    let v18: u32 = (((((v13) as u32) & ((v17) as u32)) as u32) & 0xffu32);
    let v19: u32 = (((((v18) as u32) & ((v16) as u32)) as u32) & 0xffu32);
    let v20: u32 = (((((v15) as u32) | ((v19) as u32)) as u32) & 0xffu32);
    let v21: u32 = (((((v20) as u32) >> 7) as u32) & 0x1u32);
    let v22: bool = (((0x0u32) as u32) == ((v21) as u32));
    let v23: bool = (!(v22));
    let v24: u32 = (if (v23) { ((0x1u32) as u32) } else { ((0x0u32) as u32) });
    let v25: u64 = (((((c as u64)) >> 8) as u64) & 0xffffffffffffffu64);
    let v26: u32 = v24;
    let v27: u64 = v25;
    let v28: u64 = (((((v27) as u64) << 8) | ((v26) as u64)) as u64);
    ((v28) as u64)
}
