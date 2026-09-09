#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of control__E01603__rust_regen_1655.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(15, 0, v0), Extract(7, 0, v1), 0)
#[no_mangle]
pub extern "C" fn emu_control__E01603__rust_regen_1655(a: u8, b: u16) -> u32
{
    ((((((((b as u32)) as u32) << 16) | ((((a as u32)) as u32) << 8) | ((0x0u32) as u32)) as u32)) as u32)
}
