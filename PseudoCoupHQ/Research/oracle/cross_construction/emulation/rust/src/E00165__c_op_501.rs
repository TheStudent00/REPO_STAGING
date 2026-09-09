#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00165__c_op_501.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(And(fpEQ(fpToFP(fp.to_ieee_bv(fpToFP(RNE(), Extract(31, 0, v0)))), fpToFP(Extract(31, 0, v1))), Not(Or(fpIsNaN(fpToFP(fp.to_ieee_bv(fpToFP(RNE(), Extract(31, 0, v0))))), fpIsNaN(fpToFP(Extract(31, 0, v1)))))), 0, 1))
#[no_mangle]
pub extern "C" fn emu_E00165__c_op_501(a: u32, b: f32, c: f64) -> u32
{
    (((((((0x0u32) as u32) << 1) | (((if (((((b) == (f32::from_bits(((((((((a as u32)) as i32)) as f32)).to_bits() as u32)) as u32)))) && ((!(((((b) != (b))) || (((f32::from_bits(((((((((a as u32)) as i32)) as f32)).to_bits() as u32)) as u32)) != (f32::from_bits(((((((((a as u32)) as i32)) as f32)).to_bits() as u32)) as u32)))))))))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u32)) as u32)) as u32)
}
