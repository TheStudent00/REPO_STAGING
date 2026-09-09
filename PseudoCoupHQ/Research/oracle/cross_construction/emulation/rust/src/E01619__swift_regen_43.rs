#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E01619__swift_regen_43.
// The term's layer-5 text, LITERAL:
//   Concat(0, 255*Extract(7, 0, v0))
#[no_mangle]
pub extern "C" fn emu_E01619__swift_regen_43(a: u8) -> u32
{
    (((((((0x0u32) as u32) << 8) | (((((((((a as u32)) as u32)).wrapping_mul(((0xffu32) as u32))) as u32) & 0xffu32)) as u32)) as u32)) as u32)
}
