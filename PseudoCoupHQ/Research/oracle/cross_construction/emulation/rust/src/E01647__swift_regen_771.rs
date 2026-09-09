#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E01647__swift_regen_771.
// The term's layer-5 text, LITERAL:
//   ~(If(0 <= Extract(7, 0, v0), 254, 255) | If(ULE(Extract(15, 0, v1), Extract(15, 0, v0)), 254, 255))
#[no_mangle]
pub extern "C" fn emu_E01647__swift_regen_771(a: u16, b: u16, c: u64) -> u8
{
    (((((!((((((((if ((((((((0x0u32) as u32) << 24) as i32) >> 24)) <= (((((((((((b as u32)) >> 0) as u32) & 0xffu32)) as u32) << 24) as i32) >> 24)))) { ((0xfeu32) as u32) } else { ((0xffu32) as u32) })) as u32) | (((if ((((((a as u32)) as u32)) <= ((((b as u32)) as u32)))) { ((0xfeu32) as u32) } else { ((0xffu32) as u32) })) as u32)) as u32) & 0xffu32)) as u32)) as u32) & 0xffu32)) as u8)
}
