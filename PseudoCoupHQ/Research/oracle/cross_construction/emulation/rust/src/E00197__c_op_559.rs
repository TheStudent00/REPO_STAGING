#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00197__c_op_559.
// The term's layer-5 text, LITERAL:
//   If(And(Not(fpToFP(Extract(63, 0, v0)) < fpToFP(fp.to_ieee_bv(fpToFP(RNE(), v1)))), Not(fpEQ(fpToFP(Extract(63, 0, v0)), fpToFP(fp.to_ieee_bv(fpToFP(RNE(), v1))))), Not(Or(fpIsNaN(fpToFP(Extract(63, 0, v0))), fpIsNaN(fpToFP(fp.to_ieee_bv(fpToFP(RNE(), v1))))))), 1, 0)
#[no_mangle]
pub extern "C" fn emu_E00197__c_op_559(a: u64, b: f64, c: f64) -> u8
{
    (((if ((((!(((b) == (f64::from_bits(((((((((a as u64)) as i64)) as f64)).to_bits() as u64)) as u64)))))) && ((!(((b) < (f64::from_bits(((((((((a as u64)) as i64)) as f64)).to_bits() as u64)) as u64)))))) && ((!(((((b) != (b))) || (((f64::from_bits(((((((((a as u64)) as i64)) as f64)).to_bits() as u64)) as u64)) != (f64::from_bits(((((((((a as u64)) as i64)) as f64)).to_bits() as u64)) as u64)))))))))) { ((0x1u32) as u32) } else { ((0x0u32) as u32) })) as u8)
}
