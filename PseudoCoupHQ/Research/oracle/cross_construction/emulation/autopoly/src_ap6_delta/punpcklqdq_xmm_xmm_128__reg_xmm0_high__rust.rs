#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of punpcklqdq_xmm_xmm_128__reg_xmm0_high__rust.
// The term's layer-5 text, LITERAL:
//   Extract(63, 0, v0)
#[no_mangle]
pub extern "C" fn emu_punpcklqdq_xmm_xmm_128__reg_xmm0_high__rust(a: f64) -> f64
{
    f64::from_bits((((a).to_bits() as u64)) as u64)
}
