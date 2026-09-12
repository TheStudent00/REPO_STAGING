#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of fcvt_d_wu_fpr_gpr_64__freg_fa0__rust__native_first.
//   fp.to_ieee_bv(fpToFPUnsigned(RNE(), Extract(31, 0, v0)))
#[no_mangle]
pub extern "C" fn emu_fcvt_d_wu_fpr_gpr_64__freg_fa0__rust__native_first(a: u32) -> u64
{
    let v0: u32 = (a as u32);
    let v1: f64 = (((v0) as u32) as f64);
    let v2: u64 = ((v1).to_bits() as u64);
    ((v2) as u64)
}
