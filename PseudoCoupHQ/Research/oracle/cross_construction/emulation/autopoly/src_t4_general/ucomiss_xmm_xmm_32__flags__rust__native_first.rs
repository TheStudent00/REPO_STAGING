#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of ucomiss_xmm_xmm_32__flags__rust__native_first.
//   Concat(fp.to_ieee_bv(fpToFP(Extract(31, 0, v0))), fp.to_ieee_bv(fpToFP(Extract(31, 0, v1))))
#[no_mangle]
pub extern "C" fn emu_ucomiss_xmm_xmm_32__flags__rust__native_first(a: f32, b: f32) -> u64
{
    let v1: f32 = b;
    let v2: u32 = ((v1).to_bits() as u32);
    let v4: f32 = a;
    let v5: u32 = ((v4).to_bits() as u32);
    let v6: u64 = (((((v5) as u64) << 32) | ((v2) as u64)) as u64);
    ((v6) as u64)
}
