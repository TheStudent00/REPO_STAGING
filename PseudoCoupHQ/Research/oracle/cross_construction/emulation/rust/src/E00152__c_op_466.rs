#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00152__c_op_466.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(And(fpEQ(fpToFP(fp.to_ieee_bv(fpToFP(RNE(), Extract(31, 0, v0)))), fpToFP(Extract(63, 0, v1))), Not(Or(fpIsNaN(fpToFP(Extract(63, 0, v1))), fpIsNaN(fpToFP(fp.to_ieee_bv(fpToFP(RNE(), Extract(31, 0, v0)))))))), 1, 0))
#[no_mangle]
pub extern "C" fn emu_E00152__c_op_466(a: u32, b: f64, c: f64) -> u32
{
    (((((((0x0u32) as u32) << 1) | (((if (((((b) == (f64::from_bits(((((((((a as u32)) as i32)) as f64)).to_bits() as u64)) as u64)))) && ((!(((((b) != (b))) || (((f64::from_bits(((((((((a as u32)) as i32)) as f64)).to_bits() as u64)) as u64)) != (f64::from_bits(((((((((a as u32)) as i32)) as f64)).to_bits() as u64)) as u64)))))))))) { ((0x1u32) as u32) } else { ((0x0u32) as u32) })) as u32)) as u32)) as u32)
}
