#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of slti_gpr_gpr_imm_64__reg_a0__rust__native_first.
//   If(3 <= v0, 0, 1)
#[no_mangle]
pub extern "C" fn emu_slti_gpr_gpr_imm_64__reg_a0__rust__native_first(a: u64) -> u64
{
    let v0: bool = ((((0x3u64) as i64)) <= ((((a as u64)) as i64)));
    let v1: u64 = (if (v0) { ((0x0u64) as u64) } else { ((0x1u64) as u64) });
    ((v1) as u64)
}
