#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of srli_gpr_gpr_imm_64__reg_a0__rust__native_first.
//   Concat(0, Extract(63, 3, v0))
#[no_mangle]
pub extern "C" fn emu_srli_gpr_gpr_imm_64__reg_a0__rust__native_first(a: u64) -> u64
{
    let v0: u64 = (((((a as u64)) >> 3) as u64) & 0x1fffffffffffffffu64);
    let v1: u64 = (((((0x0u32) as u64) << 61) | ((v0) as u64)) as u64);
    ((v1) as u64)
}
