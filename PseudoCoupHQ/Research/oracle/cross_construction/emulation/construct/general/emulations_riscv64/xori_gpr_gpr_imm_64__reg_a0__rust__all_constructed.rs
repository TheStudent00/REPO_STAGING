#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of xori_gpr_gpr_imm_64__reg_a0__rust__all_constructed.
//   Concat(Extract(63, 2, v0), ~Extract(1, 0, v0))
#[no_mangle]
pub extern "C" fn emu_xori_gpr_gpr_imm_64__reg_a0__rust__all_constructed(a: u64) -> u64
{
    let v0: u32 = (((((a as u64)) >> 0) as u32) & 0x3u32);
    let v1: u32 = (((!((v0) as u32)) as u32) & 0x3u32);
    let v2: u64 = (((((a as u64)) >> 2) as u64) & 0x3fffffffffffffffu64);
    let v3: u32 = v1;
    let v4: u64 = v2;
    let v5: u64 = (((((v4) as u64) << 2) | ((v3) as u64)) as u64);
    ((v5) as u64)
}
