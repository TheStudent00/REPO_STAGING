#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00031__c_op_112.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(fpToFP(fp.to_ieee_bv(fpToFP(RNE(), v1))) + fpToFP(Extract(63, 0, v0)))
#[no_mangle]
pub extern "C" fn emu_E00031__c_op_112(a: u64, b: f64, c: f64) -> f64
{
    f64::from_bits((((((b) + (f64::from_bits(((((((((a as u64)) as i64)) as f64)).to_bits() as u64)) as u64)))).to_bits() as u64)) as u64)
}
