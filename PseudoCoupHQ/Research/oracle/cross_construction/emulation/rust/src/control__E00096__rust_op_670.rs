#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of control__E00096__rust_op_670.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(fpToFP(Extract(63, 0, v0)) / fpToFP(Extract(63, 0, v1)))
#[no_mangle]
pub extern "C" fn emu_control__E00096__rust_op_670(a: f64, b: f64) -> f64
{
    f64::from_bits((((((a) / (b))).to_bits() as u64)) as u64)
}
