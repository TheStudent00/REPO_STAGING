#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E01653__swift_regen_1012.
// The term's layer-5 text, LITERAL:
//   If(Extract(31, 0, v0) == Extract(31, 0, v1), 0, 1) | If(0 <= Extract(31, 0, v0), 0, 1)
#[no_mangle]
pub extern "C" fn emu_E01653__swift_regen_1012(a: u32, b: u32, c: u64) -> u8
{
    ((((((((if (((((a as u32)) as u32) == (((b as u32)) as u32))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u32) | (((if (((((0x0u32) as i32)) <= ((((a as u32)) as i32)))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u32)) as u32) & 0xffu32)) as u8)
}
