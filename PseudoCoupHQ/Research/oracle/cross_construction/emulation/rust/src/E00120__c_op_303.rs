#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00120__c_op_303.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(And(fpEQ(fpToFP(Extract(31, 0, v0)), +0.0), Not(fpIsNaN(fpToFP(Extract(31, 0, v0))))), 0, 1) | If(And(fpEQ(fpToFP(Extract(31, 0, v1)), +0.0), Not(fpIsNaN(fpToFP(Extract(31, 0, v1))))), 0, 1))
#[no_mangle]
pub extern "C" fn emu_E00120__c_op_303(a: f32, b: f32, c: f64) -> u32
{
    (((((((0x0u32) as u32) << 1) | ((((((((if (((((a) == ((0.0f32)))) && ((!(((a) != (a))))))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u32) | (((if (((((b) == ((0.0f32)))) && ((!(((b) != (b))))))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u32)) as u32) & 0x1u32)) as u32)) as u32)) as u32)
}
