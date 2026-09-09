#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00169__c_op_508.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(And(fpEQ(fpToFP(fp.to_ieee_bv(fpToFP(RNE(), v0))), fpToFP(Extract(63, 0, v1))), Not(Or(fpIsNaN(fpToFP(fp.to_ieee_bv(fpToFP(RNE(), v0)))), fpIsNaN(fpToFP(Extract(63, 0, v1)))))), 0, 1))
#[no_mangle]
pub extern "C" fn emu_E00169__c_op_508(a: u64, b: f64, c: f64) -> u32
{
    (((((((0x0u32) as u32) << 1) | (((if (((((b) == (f64::from_bits(((((((((a as u64)) as i64)) as f64)).to_bits() as u64)) as u64)))) && ((!(((((b) != (b))) || (((f64::from_bits(((((((((a as u64)) as i64)) as f64)).to_bits() as u64)) as u64)) != (f64::from_bits(((((((((a as u64)) as i64)) as f64)).to_bits() as u64)) as u64)))))))))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u32)) as u32)) as u32)
}
