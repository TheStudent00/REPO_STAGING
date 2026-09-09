#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of cmpneqsd_xmm_xmm_64__reg_xmm0__rust.
// The term's layer-5 text, LITERAL:
//   If(And(fpEQ(fpToFP(Extract(63, 0, v0)), fpToFP(Extract(63, 0, v1))), Not(Or(fpIsNaN(fpToFP(Extract(63, 0, v0))), fpIsNaN(fpToFP(Extract(63, 0, v1)))))), 0, 18446744073709551615)
#[no_mangle]
pub extern "C" fn emu_cmpneqsd_xmm_xmm_64__reg_xmm0__rust(a: f64, b: f64) -> f64
{
    f64::from_bits(((if (((((a) == (b))) && ((!(((((a) != (a))) || (((b) != (b))))))))) { ((0x0u64) as u64) } else { ((0xffffffffffffffffu64) as u64) })) as u64)
}
