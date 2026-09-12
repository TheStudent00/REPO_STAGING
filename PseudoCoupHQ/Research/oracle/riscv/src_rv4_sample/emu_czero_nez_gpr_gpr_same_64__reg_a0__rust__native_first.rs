#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of czero_nez_gpr_gpr_same_64__reg_a0__rust__native_first.
//   If(v0 == 0, v0, 0)
#[no_mangle]
pub extern "C" fn emu_czero_nez_gpr_gpr_same_64__reg_a0__rust__native_first(a: u64) -> u64
{
    let v0: bool = ((((a as u64)) as u64) == ((0x0u64) as u64));
    let v1: u64 = (if (v0) { (((a as u64)) as u64) } else { ((0x0u64) as u64) });
    ((v1) as u64)
}
