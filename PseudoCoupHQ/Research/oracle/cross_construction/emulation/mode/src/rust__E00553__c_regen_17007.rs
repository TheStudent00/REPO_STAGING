#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o13 emulation WITH THE MODE -- rendered by mode.py
// ModeRendererRust from the layer-4 term of rust__E00553__c_regen_17007,
// and from the guard the reference read off the x unit's own body.
// The term's layer-5 text, LITERAL:
//   If(Extract(7, 0, v0) | Extract(7, 0, v1) == 0, 0, 1)
#[no_mangle]
pub extern "C" fn emu_rust__E00553__c_regen_17007(a: u8, b: u8) -> u8
{
    (((if ((((((((((a as u32)) as u32) | (((b as u32)) as u32)) as u32) & 0xffu32)) as u32) == ((0x0u32) as u32))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u8)
}
