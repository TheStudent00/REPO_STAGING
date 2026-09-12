#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of fcvt_s_l_fpr_gpr_32__freg_fa0__rust__native_first.
//   Concat(4294967295, fp.to_ieee_bv(fpToFP(RNE(), v0)))
#[no_mangle]
pub extern "C" fn emu_fcvt_s_l_fpr_gpr_32__freg_fa0__rust__native_first(a: u64) -> u64
{
    let v0: f32 = (((((a as u64)) as i64)) as f32);
    let v1: u32 = ((v0).to_bits() as u32);
    let v2: u64 = (((((0xffffffffu32) as u64) << 32) | ((v1) as u64)) as u64);
    ((v2) as u64)
}
