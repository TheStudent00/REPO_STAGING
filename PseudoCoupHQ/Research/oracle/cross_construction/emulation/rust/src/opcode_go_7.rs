#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of opcode_go_7.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 32, v0), fp.to_ieee_bv(fpToFP(Extract(31, 0, v0)) / fpToFP(Extract(31, 0, v1))))
#[no_mangle]
pub extern "C" fn emu_opcode_go_7(a: f64, b: f32) -> f32
{
    f32::from_bits((((((((((((a).to_bits() as u64)) >> 32) as u32)) as u64) << 32) | ((((((f32::from_bits(((((((a).to_bits() as u64)) >> 0) as u32)) as u32)) / (b))).to_bits() as u32)) as u64)) as u64)) as u32)
}
