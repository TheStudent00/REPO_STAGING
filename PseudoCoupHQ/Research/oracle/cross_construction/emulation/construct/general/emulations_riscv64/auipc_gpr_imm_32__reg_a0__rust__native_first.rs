#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of auipc_gpr_imm_32__reg_a0__rust__native_first.
//   v0 + 12288
#[no_mangle]
pub extern "C" fn emu_auipc_gpr_imm_32__reg_a0__rust__native_first(a: u64) -> u64
{
    let v0: u64 = ((((((a as u64)) as u64)).wrapping_add(((0x3000u64) as u64))) as u64);
    ((v0) as u64)
}
