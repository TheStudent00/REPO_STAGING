#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00118__c_op_307.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(v1 == 0, 0, 1) | If(fpIsNaN(fpToFP(Extract(63, 0, v0))), 1, 0) | If(Or(Not(fpEQ(fpToFP(Extract(63, 0, v0)), +0.0)), fpIsNaN(fpToFP(Extract(63, 0, v0)))), 1, 0))
#[no_mangle]
pub extern "C" fn emu_E00118__c_op_307(a: u64, b: u64, c: f64, d: f64) -> u32
{
    (((((((0x0u32) as u32) << 8) | ((((((((if (((((a as u64)) as u64) == ((0x0u64) as u64))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u32) | (((if (((c) != (c))) { ((0x1u32) as u32) } else { ((0x0u32) as u32) })) as u32) | (((if (((((c) != (c))) || ((!(((c) == ((0.0f64)))))))) { ((0x1u32) as u32) } else { ((0x0u32) as u32) })) as u32)) as u32) & 0xffu32)) as u32)) as u32)) as u32)
}
