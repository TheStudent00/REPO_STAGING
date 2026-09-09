#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of movss_mem_xmm_32__reg_xmm0__rust.
// The term's layer-5 text, LITERAL:
//   Extract(31, 0, v0)
#[no_mangle]
pub extern "C" fn emu_movss_mem_xmm_32__reg_xmm0__rust(a: u32) -> f32
{
    f32::from_bits(((a as u32)) as u32)
}
