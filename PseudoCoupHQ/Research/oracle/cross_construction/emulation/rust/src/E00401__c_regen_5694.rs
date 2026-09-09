#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00401__c_regen_5694.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 32, v1), fp.to_ieee_bv(-fpToFP(fp.to_ieee_bv(fpToFP(RNE(), Concat(0, Extract(31, 0, v0))))) + fpToFP(Extract(31, 0, v1))))
#[no_mangle]
pub extern "C" fn emu_E00401__c_regen_5694(a: u32, b: f64, c: f64) -> f32
{
    f32::from_bits((((((((((((b).to_bits() as u64)) >> 32) as u32)) as u64) << 32) | (((((((-(f32::from_bits(((((((((((((0x0u32) as u64) << 32) | (((a as u32)) as u64)) as u64)) as i64)) as f32)).to_bits() as u32)) as u32)))) + (f32::from_bits(((((((b).to_bits() as u64)) >> 0) as u32)) as u32)))).to_bits() as u32)) as u64)) as u64)) as u32)
}
