#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E01831__swift_regen_2633.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(7, 0, v0), Extract(7, 0, v1))
#[no_mangle]
pub extern "C" fn emu_E01831__swift_regen_2633(a: u8, b: u8) -> u32
{
    (((((((0x0u32) as u32) << 16) | ((((b as u32)) as u32) << 8) | (((a as u32)) as u32)) as u32)) as u32)
}
