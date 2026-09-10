#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of punpckldq_mem_xmm_128__reg_xmm0_high__rust.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 32, v0), Extract(63, 32, v1))
#[no_mangle]
pub extern "C" fn emu_punpckldq_mem_xmm_128__reg_xmm0_high__rust(a: u64, b: f64) -> f64
{
    f64::from_bits(((((((((((a as u64)) >> 32) as u32)) as u64) << 32) | (((((((b).to_bits() as u64)) >> 32) as u32)) as u64)) as u64)) as u64)
}
