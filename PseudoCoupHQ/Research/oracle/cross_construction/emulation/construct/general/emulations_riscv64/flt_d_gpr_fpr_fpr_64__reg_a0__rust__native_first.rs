#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of flt_d_gpr_fpr_fpr_64__reg_a0__rust__native_first.
//   If(fpToFP(v0) < fpToFP(v1), 1, 0)
#[no_mangle]
pub extern "C" fn emu_flt_d_gpr_fpr_fpr_64__reg_a0__rust__native_first(a: u64, b: u64) -> u64
{
    let v0: f64 = f64::from_bits(((b as u64)) as u64);
    let v1: f64 = f64::from_bits(((a as u64)) as u64);
    let v2: bool = ((v1) < (v0));
    let v3: u64 = (if (v2) { ((0x1u64) as u64) } else { ((0x0u64) as u64) });
    ((v3) as u64)
}
