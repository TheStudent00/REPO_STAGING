#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of opcode_swift_15.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(7, 1, v0), ~Extract(0, 0, v0))
#[no_mangle]
pub extern "C" fn emu_opcode_swift_15(a: u8) -> u8
{
    (((((((((((((a as u32)) >> 1) as u32) & 0x7fu32)) as u32) << 1) | (((((!(((((((a as u32)) >> 0) as u32) & 0x1u32)) as u32)) as u32) & 0x1u32)) as u32)) as u32) & 0xffu32)) as u8)
}
