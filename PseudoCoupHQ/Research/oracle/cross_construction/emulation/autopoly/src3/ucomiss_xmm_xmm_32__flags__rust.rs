#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of ucomiss_xmm_xmm_32__flags__rust.
// The term's layer-5 text, LITERAL:
//   Concat(fp.to_ieee_bv(fpToFP(Extract(31, 0, v0))), fp.to_ieee_bv(fpToFP(Extract(31, 0, v1))))
#[no_mangle]
pub extern "C" fn emu_ucomiss_xmm_xmm_32__flags__rust(a: f32, b: f32) -> u64
{
    (((((((((a).to_bits() as u32)) as u64) << 32) | ((((b).to_bits() as u32)) as u64)) as u64)) as u64)
}
