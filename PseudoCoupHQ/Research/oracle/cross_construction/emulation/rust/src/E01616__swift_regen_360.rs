#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E01616__swift_regen_360.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(15, 0, v0) + 65535*Extract(15, 0, v1))
#[no_mangle]
pub extern "C" fn emu_E01616__swift_regen_360(a: u16, b: u16) -> u32
{
    (((((((0x0u32) as u32) << 16) | (((((((((((((((b as u32)) as u32)).wrapping_mul(((0xffffu32) as u32))) as u32) & 0xffffu32)) as u32)).wrapping_add((((a as u32)) as u32))) as u32) & 0xffffu32)) as u32)) as u32)) as u32)
}
