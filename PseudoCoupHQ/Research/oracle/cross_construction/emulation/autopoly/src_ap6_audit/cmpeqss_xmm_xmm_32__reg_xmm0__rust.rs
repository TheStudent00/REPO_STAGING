#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of cmpeqss_xmm_xmm_32__reg_xmm0__rust.
// The term's layer-5 text, LITERAL:
//   If(And(fpEQ(fpToFP(Extract(31, 0, v0)), fpToFP(Extract(31, 0, v1))), Not(Or(fpIsNaN(fpToFP(Extract(31, 0, v0))), fpIsNaN(fpToFP(Extract(31, 0, v1)))))), 4294967295, 0)
#[no_mangle]
pub extern "C" fn emu_cmpeqss_xmm_xmm_32__reg_xmm0__rust(a: f32, b: f32) -> f32
{
    f32::from_bits(((if (((((a) == (b))) && ((!(((((a) != (a))) || (((b) != (b))))))))) { ((0xffffffffu32) as u32) } else { ((0x0u32) as u32) })) as u32)
}
