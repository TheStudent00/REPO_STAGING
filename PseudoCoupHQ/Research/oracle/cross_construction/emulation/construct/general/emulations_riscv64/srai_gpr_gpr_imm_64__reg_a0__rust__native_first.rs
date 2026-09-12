#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of srai_gpr_gpr_imm_64__reg_a0__rust__native_first.
//   v0 >> 3
#[no_mangle]
pub extern "C" fn emu_srai_gpr_gpr_imm_64__reg_a0__rust__native_first(a: u64) -> u64
{
    let v0: u64 = ((((((a as u64)) as i64)).wrapping_shr((((0x3u64) as u64) as u32))) as u64);
    ((v0) as u64)
}
