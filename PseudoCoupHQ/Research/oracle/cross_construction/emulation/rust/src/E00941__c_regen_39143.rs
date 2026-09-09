#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00941__c_regen_39143.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(v0 <= v1, 1, 0))
#[no_mangle]
pub extern "C" fn emu_E00941__c_regen_39143(a: u64, b: u64, c: u64, d: u64) -> u32
{
    (((((((0x0u32) as u32) << 8) | (((if ((((((d as u64)) as i64)) <= ((((b as u64)) as i64)))) { ((0x1u32) as u32) } else { ((0x0u32) as u32) })) as u32)) as u32)) as u32)
}
