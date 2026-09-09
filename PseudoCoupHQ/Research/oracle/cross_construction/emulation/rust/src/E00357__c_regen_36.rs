#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00357__c_regen_36.
// The term's layer-5 text, LITERAL:
//   If(Extract(15, 0, v0) == 0, 1, 0)
#[no_mangle]
pub extern "C" fn emu_E00357__c_regen_36(a: u16) -> u8
{
    (((if (((((a as u32)) as u32) == ((0x0u32) as u32))) { ((0x1u32) as u32) } else { ((0x0u32) as u32) })) as u8)
}
