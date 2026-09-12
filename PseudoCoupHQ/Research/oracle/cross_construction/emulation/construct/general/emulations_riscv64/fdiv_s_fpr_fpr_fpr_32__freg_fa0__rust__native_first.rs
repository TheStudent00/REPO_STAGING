#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of fdiv_s_fpr_fpr_fpr_32__freg_fa0__rust__native_first.
//   Concat(4294967295, fp.to_ieee_bv(fpToFP(Extract(31, 0, v0)) / fpToFP(Extract(31, 0, v1))))
#[no_mangle]
pub extern "C" fn emu_fdiv_s_fpr_fpr_fpr_32__freg_fa0__rust__native_first(a: u32, b: u32) -> u64
{
    let v0: u32 = (b as u32);
    let v1: f32 = f32::from_bits((v0) as u32);
    let v2: u32 = (a as u32);
    let v3: f32 = f32::from_bits((v2) as u32);
    let v4: f32 = ((v3) / (v1));
    let v5: u32 = ((v4).to_bits() as u32);
    let v6: u64 = (((((0xffffffffu32) as u64) << 32) | ((v5) as u64)) as u64);
    ((v6) as u64)
}
