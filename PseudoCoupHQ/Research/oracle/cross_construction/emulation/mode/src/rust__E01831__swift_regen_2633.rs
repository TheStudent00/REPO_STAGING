#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o13 emulation WITH THE MODE -- rendered by mode.py
// ModeRendererRust from the layer-4 term of rust__E01831__swift_regen_2633,
// and from the guard the reference read off the x unit's own body.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(7, 0, v0), Extract(7, 0, v1))
#[no_mangle]
pub extern "C" fn emu_rust__E01831__swift_regen_2633(a: u8, b: u8) -> u32
{
    if ((true) && (((((((((b as u32)) as u32) << 24) as i32) >> 24)) < (((((((a as u32)) as u32) << 24) as i32) >> 24))))) { unsafe { core::arch::asm!("ud2", options(noreturn)) }; }
    (((((((0x0u32) as u32) << 16) | ((((b as u32)) as u32) << 8) | (((a as u32)) as u32)) as u32)) as u32)
}
