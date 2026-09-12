#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of bne_gpr_gpr_same_64__branch_condition__rust__all_constructed.
//   If(v0 == v1, 0, 1)
#[no_mangle]
pub extern "C" fn emu_bne_gpr_gpr_same_64__branch_condition__rust__all_constructed(a: u64, b: u64) -> u64
{
    let v0: u64 = (((((a as u64)) as u64) ^ (((b as u64)) as u64)) as u64);
    let v1: u64 = ((((v0) as u64).wrapping_shr((((0x1u64) as u64) as u32))) as u64);
    let v2: u64 = ((((v0) as u64) | ((v1) as u64)) as u64);
    let v3: u64 = ((((v2) as u64).wrapping_shr((((0x2u64) as u64) as u32))) as u64);
    let v4: u64 = ((((v2) as u64) | ((v3) as u64)) as u64);
    let v5: u64 = ((((v4) as u64).wrapping_shr((((0x4u64) as u64) as u32))) as u64);
    let v6: u64 = ((((v4) as u64) | ((v5) as u64)) as u64);
    let v7: u64 = ((((v6) as u64).wrapping_shr((((0x8u64) as u64) as u32))) as u64);
    let v8: u64 = ((((v6) as u64) | ((v7) as u64)) as u64);
    let v9: u64 = ((((v8) as u64).wrapping_shr((((0x10u64) as u64) as u32))) as u64);
    let v10: u64 = ((((v8) as u64) | ((v9) as u64)) as u64);
    let v11: u64 = ((((v10) as u64).wrapping_shr((((0x20u64) as u64) as u32))) as u64);
    let v12: u64 = ((((v10) as u64) | ((v11) as u64)) as u64);
    let v13: u32 = (((((v12) as u64) >> 0) as u32) & 0x1u32);
    let v14: bool = (((0x1u32) as u32) == ((v13) as u32));
    let v15: bool = (!(v14));
    let v16: u64 = (if (v15) { ((0x0u64) as u64) } else { ((0x1u64) as u64) });
    ((v16) as u64)
}
