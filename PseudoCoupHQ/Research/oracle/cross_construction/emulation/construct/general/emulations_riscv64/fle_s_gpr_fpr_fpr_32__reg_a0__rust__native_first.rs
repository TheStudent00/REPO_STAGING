#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of fle_s_gpr_fpr_fpr_32__reg_a0__rust__native_first.
//   If(fpToFP(Extract(31, 0, v0)) <= fpToFP(Extract(31, 0, v1)), 1, 0)
#[no_mangle]
pub extern "C" fn emu_fle_s_gpr_fpr_fpr_32__reg_a0__rust__native_first(a: u32, b: u32) -> u64
{
    let v0: u32 = (b as u32);
    let v1: f32 = f32::from_bits((v0) as u32);
    let v2: u32 = (a as u32);
    let v3: f32 = f32::from_bits((v2) as u32);
    let v4: bool = ((v3) <= (v1));
    let v5: u64 = (if (v4) { ((0x1u64) as u64) } else { ((0x0u64) as u64) });
    ((v5) as u64)
}
