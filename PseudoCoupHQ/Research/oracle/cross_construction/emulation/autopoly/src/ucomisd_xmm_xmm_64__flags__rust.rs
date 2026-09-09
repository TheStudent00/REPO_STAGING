#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of ucomisd_xmm_xmm_64__flags__rust.
// The term's layer-5 text, LITERAL:
//   Concat(fp.to_ieee_bv(fpToFP(Extract(63, 0, v0))), fp.to_ieee_bv(fpToFP(Extract(63, 0, v1))))
#[no_mangle]
pub extern "C" fn emu_ucomisd_xmm_xmm_64__flags__rust(a: f64, b: f64) -> u128
{
    (((((((((a).to_bits() as u64)) as u128) << 64) | ((((b).to_bits() as u64)) as u128)) as u128)) as u128)
}
