#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of cmpeqsd_mem_xmm_64__reg_xmm0__rust.
// The term's layer-5 text, LITERAL:
//   If(And(fpEQ(fpToFP(Extract(63, 0, v0)), fpToFP(v1)), Not(Or(fpIsNaN(fpToFP(Extract(63, 0, v0))), fpIsNaN(fpToFP(v1))))), 18446744073709551615, 0)
#[no_mangle]
pub extern "C" fn emu_cmpeqsd_mem_xmm_64__reg_xmm0__rust(a: u64, b: f64) -> f64
{
    f64::from_bits(((if (((((b) == (f64::from_bits(((a as u64)) as u64)))) && ((!(((((b) != (b))) || (((f64::from_bits(((a as u64)) as u64)) != (f64::from_bits(((a as u64)) as u64)))))))))) { ((0xffffffffffffffffu64) as u64) } else { ((0x0u64) as u64) })) as u64)
}
