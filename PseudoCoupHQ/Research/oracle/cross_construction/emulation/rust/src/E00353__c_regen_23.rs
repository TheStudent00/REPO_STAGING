#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00353__c_regen_23.
// The term's layer-5 text, LITERAL:
//   If(Extract(7, 0, v0) == 0, 1, 0)
#[no_mangle]
pub extern "C" fn emu_E00353__c_regen_23(a: u8) -> u8
{
    (((if (((((a as u32)) as u32) == ((0x0u32) as u32))) { ((0x1u32) as u32) } else { ((0x0u32) as u32) })) as u8)
}
