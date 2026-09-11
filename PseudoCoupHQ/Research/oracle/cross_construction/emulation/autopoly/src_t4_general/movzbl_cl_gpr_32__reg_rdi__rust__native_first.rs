#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of movzbl_cl_gpr_32__reg_rdi__rust__native_first.
//   Concat(0, Extract(7, 0, v0))
#[no_mangle]
pub extern "C" fn emu_movzbl_cl_gpr_32__reg_rdi__rust__native_first(a: u8) -> u64
{
    let v0: u32 = (a as u32);
    let v1: u64 = (((((0x0u64) as u64) << 8) | ((v0) as u64)) as u64);
    ((v1) as u64)
}
