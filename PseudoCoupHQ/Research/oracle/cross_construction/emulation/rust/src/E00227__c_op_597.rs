#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00227__c_op_597.
// The term's layer-5 text, LITERAL:
//   If(And(Not(fpToFP(Extract(63, 0, v1)) < fpToFP(fp.to_ieee_bv(fpToFP(RNE(), fpToFP(Extract(31, 0, v0)))))), Not(Or(fpIsNaN(fpToFP(Extract(63, 0, v1))), fpIsNaN(fpToFP(fp.to_ieee_bv(fpToFP(RNE(), fpToFP(Extract(31, 0, v0))))))))), 1, 0)
#[no_mangle]
pub extern "C" fn emu_E00227__c_op_597(a: f64, b: f32) -> u8
{
    (((if ((((!(((a) < (f64::from_bits((((((b) as f64)).to_bits() as u64)) as u64)))))) && ((!(((((a) != (a))) || (((f64::from_bits((((((b) as f64)).to_bits() as u64)) as u64)) != (f64::from_bits((((((b) as f64)).to_bits() as u64)) as u64)))))))))) { ((0x1u32) as u32) } else { ((0x0u32) as u32) })) as u8)
}
