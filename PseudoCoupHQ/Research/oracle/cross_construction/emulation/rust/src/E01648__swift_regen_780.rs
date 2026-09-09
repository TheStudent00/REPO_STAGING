#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E01648__swift_regen_780.
// The term's layer-5 text, LITERAL:
//   ~(If(0 <= Extract(15, 0, v0), 254, 255) | If(ULE(Extract(31, 0, v1), Extract(31, 0, v0)), 254, 255))
#[no_mangle]
pub extern "C" fn emu_E01648__swift_regen_780(a: u32, b: u32, c: u64) -> u8
{
    (((((!((((((((if ((((((((0x0u32) as u32) << 16) as i32) >> 16)) <= (((((((((((b as u32)) >> 0) as u32) & 0xffffu32)) as u32) << 16) as i32) >> 16)))) { ((0xfeu32) as u32) } else { ((0xffu32) as u32) })) as u32) | (((if ((((((a as u32)) as u32)) <= ((((b as u32)) as u32)))) { ((0xfeu32) as u32) } else { ((0xffu32) as u32) })) as u32)) as u32) & 0xffu32)) as u32)) as u32) & 0xffu32)) as u8)
}
