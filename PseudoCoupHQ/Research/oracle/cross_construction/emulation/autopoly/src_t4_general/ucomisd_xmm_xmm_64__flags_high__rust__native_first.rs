#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of ucomisd_xmm_xmm_64__flags_high__rust__native_first.
//   fp.to_ieee_bv(fpToFP(Extract(63, 0, v0)))
#[no_mangle]
pub extern "C" fn emu_ucomisd_xmm_xmm_64__flags_high__rust__native_first(a: f64) -> u64
{
    let v1: f64 = a;
    let v2: u64 = ((v1).to_bits() as u64);
    ((v2) as u64)
}
