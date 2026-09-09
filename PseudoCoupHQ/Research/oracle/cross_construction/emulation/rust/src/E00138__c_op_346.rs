#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00138__c_op_346.
// The term's layer-5 text, LITERAL:
//   ~(4294967294 | If(And(fpEQ(fpToFP(Extract(63, 0, v0)), +0.0), Not(fpIsNaN(fpToFP(Extract(63, 0, v0))))), 4294967295, 0) | If(And(fpEQ(fpToFP(Extract(63, 0, v1)), +0.0), Not(fpIsNaN(fpToFP(Extract(63, 0, v1))))), 4294967295, 0))
#[no_mangle]
pub extern "C" fn emu_E00138__c_op_346(a: f64, b: f64, c: f64) -> u32
{
    ((((!(((((((if (((((a) == ((0.0f64)))) && ((!(((a) != (a))))))) { ((0xffffffffu32) as u32) } else { ((0x0u32) as u32) })) as u32) | (((if (((((b) == ((0.0f64)))) && ((!(((b) != (b))))))) { ((0xffffffffu32) as u32) } else { ((0x0u32) as u32) })) as u32) | ((0xfffffffeu32) as u32)) as u32)) as u32)) as u32)) as u32)
}
