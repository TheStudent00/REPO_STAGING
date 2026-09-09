#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00870__c_regen_36482.
// The term's layer-5 text, LITERAL:
//   If(And(Not(fpToFP(Extract(31, 0, v1)) < fpToFP(fp.to_ieee_bv(fpToFP(RNE(), Concat(0, Extract(31, 0, v0)))))), Not(fpEQ(fpToFP(Extract(31, 0, v1)), fpToFP(fp.to_ieee_bv(fpToFP(RNE(), Concat(0, Extract(31, 0, v0))))))), Not(Or(fpIsNaN(fpToFP(Extract(31, 0, v1))), fpIsNaN(fpToFP(fp.to_ieee_bv(fpToFP(RNE(), Concat(0, Extract(31, 0, v0))))))))), 1, 0)
#[no_mangle]
pub extern "C" fn emu_E00870__c_regen_36482(a: u32, b: f32, c: f64) -> u8
{
    (((if ((((!(((b) == (f32::from_bits(((((((((((((0x0u32) as u64) << 32) | (((a as u32)) as u64)) as u64)) as i64)) as f32)).to_bits() as u32)) as u32)))))) && ((!(((b) < (f32::from_bits(((((((((((((0x0u32) as u64) << 32) | (((a as u32)) as u64)) as u64)) as i64)) as f32)).to_bits() as u32)) as u32)))))) && ((!(((((b) != (b))) || (((f32::from_bits(((((((((((((0x0u32) as u64) << 32) | (((a as u32)) as u64)) as u64)) as i64)) as f32)).to_bits() as u32)) as u32)) != (f32::from_bits(((((((((((((0x0u32) as u64) << 32) | (((a as u32)) as u64)) as u64)) as i64)) as f32)).to_bits() as u32)) as u32)))))))))) { ((0x1u32) as u32) } else { ((0x0u32) as u32) })) as u8)
}
