#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of subsd_mem_xmm_64__reg_xmm0__rust.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(-fpToFP(v0) + fpToFP(Extract(63, 0, v1)))
#[no_mangle]
pub extern "C" fn emu_subsd_mem_xmm_64__reg_xmm0__rust(a: u64, b: f64) -> f64
{
    f64::from_bits(((((((-(f64::from_bits(((a as u64)) as u64)))) + (b))).to_bits() as u64)) as u64)
}
