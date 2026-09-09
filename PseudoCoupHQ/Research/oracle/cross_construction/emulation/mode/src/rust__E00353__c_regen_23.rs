#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o13 emulation WITH THE MODE -- rendered by mode.py
// ModeRendererRust from the layer-4 term of rust__E00353__c_regen_23,
// and from the guard the reference read off the x unit's own body.
// The term's layer-5 text, LITERAL:
//   If(Extract(7, 0, v0) == 0, 1, 0)
#[no_mangle]
pub extern "C" fn emu_rust__E00353__c_regen_23(a: u8) -> u8
{
    (((if (((((a as u32)) as u32) == ((0x0u32) as u32))) { ((0x1u32) as u32) } else { ((0x0u32) as u32) })) as u8)
}
