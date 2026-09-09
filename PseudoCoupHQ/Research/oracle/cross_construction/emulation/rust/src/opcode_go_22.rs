#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of opcode_go_22.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(-fpToFP(Extract(63, 0, v0)) + fpToFP(Extract(63, 0, v1)))
#[no_mangle]
pub extern "C" fn emu_opcode_go_22(a: f64, b: f64) -> f64
{
    f64::from_bits(((((((-(b))) + (a))).to_bits() as u64)) as u64)
}
