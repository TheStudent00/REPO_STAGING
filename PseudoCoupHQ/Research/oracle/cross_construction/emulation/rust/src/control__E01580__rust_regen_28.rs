#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of control__E01580__rust_regen_28.
// The term's layer-5 text, LITERAL:
//   ~Extract(7, 0, v0)
#[no_mangle]
pub extern "C" fn emu_control__E01580__rust_regen_28(a: u8) -> u8
{
    (((((!(((a as u32)) as u32)) as u32) & 0xffu32)) as u8)
}
