#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E01623__swift_regen_419.
// The term's layer-5 text, LITERAL:
//   If(0 <= Extract(31, 0, v0), 0, 1) | If(ULE(Extract(31, 0, v1), Extract(31, 0, v0)), 0, 1)
#[no_mangle]
pub extern "C" fn emu_E01623__swift_regen_419(a: u32, b: u32, c: u64) -> u8
{
    ((((((((if (((((0x0u32) as i32)) <= ((((a as u32)) as i32)))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u32) | (((if ((((((b as u32)) as u32)) <= ((((a as u32)) as u32)))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u32)) as u32) & 0xffu32)) as u8)
}
