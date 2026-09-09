#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00174__c_op_520.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(And(fpEQ(fpToFP(fp.to_ieee_bv(fpToFP(RNE(), fpToFP(Extract(31, 0, v0))))), fpToFP(Extract(63, 0, v1))), Not(Or(fpIsNaN(fpToFP(Extract(63, 0, v1))), fpIsNaN(fpToFP(fp.to_ieee_bv(fpToFP(RNE(), fpToFP(Extract(31, 0, v0))))))))), 0, 1))
#[no_mangle]
pub extern "C" fn emu_E00174__c_op_520(a: f32, b: f64) -> u32
{
    (((((((0x0u32) as u32) << 1) | (((if (((((b) == (f64::from_bits((((((a) as f64)).to_bits() as u64)) as u64)))) && ((!(((((b) != (b))) || (((f64::from_bits((((((a) as f64)).to_bits() as u64)) as u64)) != (f64::from_bits((((((a) as f64)).to_bits() as u64)) as u64)))))))))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u32)) as u32)) as u32)
}
