#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00546__c_regen_16844.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(v1 | v2 == 0, 0, 1) | If(fpIsNaN(fpToFP(Extract(31, 0, v0))), 1, 0) | If(Or(fpIsNaN(fpToFP(Extract(31, 0, v0))), Not(fpEQ(fpToFP(Extract(31, 0, v0)), +0.0))), 1, 0))
#[no_mangle]
pub extern "C" fn emu_E00546__c_regen_16844(a: u64, b: u64, c: u64, d: u64, e: f32, f: f64) -> u32
{
    (((((((0x0u32) as u32) << 8) | ((((((((if (((((((((a as u64)) as u64) | (((b as u64)) as u64)) as u64)) as u64) == ((0x0u64) as u64))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u32) | (((if (((e) != (e))) { ((0x1u32) as u32) } else { ((0x0u32) as u32) })) as u32) | (((if (((((e) != (e))) || ((!(((e) == ((0.0f32)))))))) { ((0x1u32) as u32) } else { ((0x0u32) as u32) })) as u32)) as u32) & 0xffu32)) as u32)) as u32)) as u32)
}
