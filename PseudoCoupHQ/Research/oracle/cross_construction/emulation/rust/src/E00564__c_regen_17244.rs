#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00564__c_regen_17244.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(Extract(15, 0, v1) == 0, 0, 1) | If(fpIsNaN(fpToFP(Extract(63, 0, v0))), 1, 0) | If(Or(fpIsNaN(fpToFP(Extract(63, 0, v0))), Not(fpEQ(fpToFP(Extract(63, 0, v0)), +0.0))), 1, 0))
#[no_mangle]
pub extern "C" fn emu_E00564__c_regen_17244(a: u16, b: u64, c: f64, d: f64) -> u32
{
    (((((((0x0u32) as u32) << 8) | ((((((((if (((((a as u32)) as u32) == ((0x0u32) as u32))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u32) | (((if (((c) != (c))) { ((0x1u32) as u32) } else { ((0x0u32) as u32) })) as u32) | (((if (((((c) != (c))) || ((!(((c) == ((0.0f64)))))))) { ((0x1u32) as u32) } else { ((0x0u32) as u32) })) as u32)) as u32) & 0xffu32)) as u32)) as u32)) as u32)
}
