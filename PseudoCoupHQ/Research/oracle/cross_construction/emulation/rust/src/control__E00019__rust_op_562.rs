#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of control__E00019__rust_op_562.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(fpToFP(Extract(63, 0, v1)) + fpToFP(Extract(63, 0, v0)))
#[no_mangle]
pub extern "C" fn emu_control__E00019__rust_op_562(a: f64, b: f64) -> f64
{
    f64::from_bits((((((a) + (b))).to_bits() as u64)) as u64)
}
