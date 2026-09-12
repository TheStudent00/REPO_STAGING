#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of subss_xmm_xmm_32__reg_xmm0__rust.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(-fpToFP(Extract(31, 0, v0)) + fpToFP(Extract(31, 0, v1)))
#[no_mangle]
pub extern "C" fn emu_subss_xmm_xmm_32__reg_xmm0__rust(a: f32, b: f32) -> f32
{
    f32::from_bits(((((((-(b))) + (a))).to_bits() as u32)) as u32)
}
