#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00937__c_regen_39171.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(0 <= v0, 1, 0))
#[no_mangle]
pub extern "C" fn emu_E00937__c_regen_39171(a: u64, b: u64, c: u64) -> u32
{
    (((((((0x0u32) as u32) << 8) | (((if (((((0x0u64) as i64)) <= ((((b as u64)) as i64)))) { ((0x1u32) as u32) } else { ((0x0u32) as u32) })) as u32)) as u32)) as u32)
}
