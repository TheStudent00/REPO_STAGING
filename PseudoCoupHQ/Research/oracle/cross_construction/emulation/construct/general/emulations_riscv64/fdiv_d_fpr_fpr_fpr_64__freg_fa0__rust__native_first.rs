#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of fdiv_d_fpr_fpr_fpr_64__freg_fa0__rust__native_first.
//   fp.to_ieee_bv(fpToFP(v0) / fpToFP(v1))
#[no_mangle]
pub extern "C" fn emu_fdiv_d_fpr_fpr_fpr_64__freg_fa0__rust__native_first(a: u64, b: u64) -> u64
{
    let v0: f64 = f64::from_bits(((b as u64)) as u64);
    let v1: f64 = f64::from_bits(((a as u64)) as u64);
    let v2: f64 = ((v1) / (v0));
    let v3: u64 = ((v2).to_bits() as u64);
    ((v3) as u64)
}
