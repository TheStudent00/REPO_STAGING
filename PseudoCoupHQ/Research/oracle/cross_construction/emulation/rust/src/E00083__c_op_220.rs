#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00083__c_op_220.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(fpToFP(fp.to_ieee_bv(fpToFP(RNE(), v0))) / fpToFP(Extract(63, 0, v1)))
#[no_mangle]
pub extern "C" fn emu_E00083__c_op_220(a: u64, b: f64, c: f64) -> f64
{
    f64::from_bits((((((f64::from_bits(((((((((a as u64)) as i64)) as f64)).to_bits() as u64)) as u64)) / (b))).to_bits() as u64)) as u64)
}
