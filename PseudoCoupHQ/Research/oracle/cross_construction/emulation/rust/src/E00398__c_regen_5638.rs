#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00398__c_regen_5638.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(-fpToFP(fp.to_ieee_bv(fpToFP(RNE(), Concat(0, Extract(31, 0, v0))))) + fpToFP(Extract(63, 0, v1)))
#[no_mangle]
pub extern "C" fn emu_E00398__c_regen_5638(a: u32, b: f64, c: f64) -> f64
{
    f64::from_bits(((((((-(f64::from_bits(((((((((((((0x0u32) as u64) << 32) | (((a as u32)) as u64)) as u64)) as i64)) as f64)).to_bits() as u64)) as u64)))) + (b))).to_bits() as u64)) as u64)
}
