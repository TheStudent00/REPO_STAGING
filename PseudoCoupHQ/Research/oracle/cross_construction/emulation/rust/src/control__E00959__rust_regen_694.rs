#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of control__E00959__rust_regen_694.
// The term's layer-5 text, LITERAL:
//   If(Extract(15, 0, v0) <= Extract(15, 0, v1), 1, 0)
#[no_mangle]
pub extern "C" fn emu_control__E00959__rust_regen_694(a: u16, b: u16) -> u8
{
    (((if (((((((((a as u32)) as u32) << 16) as i32) >> 16)) <= (((((((b as u32)) as u32) << 16) as i32) >> 16)))) { ((0x1u32) as u32) } else { ((0x0u32) as u32) })) as u8)
}
