#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00128__c_op_336.
// The term's layer-5 text, LITERAL:
//   Concat(0, ~(~(If(fpIsNaN(fpToFP(Extract(31, 0, v0))), 1, 0) | If(Or(fpIsNaN(fpToFP(Extract(31, 0, v0))), Not(fpEQ(fpToFP(Extract(31, 0, v0)), +0.0))), 1, 0)) | If(Extract(31, 0, v1) == 0, 255, 254)))
#[no_mangle]
pub extern "C" fn emu_E00128__c_op_336(a: u32, b: u64, c: f32, d: f64) -> u32
{
    (((((((0x0u32) as u32) << 8) | (((((!((((((((((!((((((((if (((c) != (c))) { ((0x1u32) as u32) } else { ((0x0u32) as u32) })) as u32) | (((if (((((c) != (c))) || ((!(((c) == ((0.0f32)))))))) { ((0x1u32) as u32) } else { ((0x0u32) as u32) })) as u32)) as u32) & 0xffu32)) as u32)) as u32) & 0xffu32)) as u32) | (((if (((((a as u32)) as u32) == ((0x0u32) as u32))) { ((0xffu32) as u32) } else { ((0xfeu32) as u32) })) as u32)) as u32) & 0xffu32)) as u32)) as u32) & 0xffu32)) as u32)) as u32)) as u32)
}
