#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00003__c_op_3.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(And(fpEQ(+0.0, fpToFP(Extract(31, 0, v0))), Not(fpIsNaN(fpToFP(Extract(31, 0, v0))))), 1, 0))
#[no_mangle]
pub extern "C" fn emu_E00003__c_op_3(a: f32, b: f64) -> u32
{
    (((((((0x0u32) as u32) << 1) | (((if (((((a) == ((0.0f32)))) && ((!(((a) != (a))))))) { ((0x1u32) as u32) } else { ((0x0u32) as u32) })) as u32)) as u32)) as u32)
}
