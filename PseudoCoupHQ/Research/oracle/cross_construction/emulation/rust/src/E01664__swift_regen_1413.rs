#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E01664__swift_regen_1413.
// The term's layer-5 text, LITERAL:
//   If(Concat(0, Extract(31, 0, v0)) == v1, 1, 0)
#[no_mangle]
pub extern "C" fn emu_E01664__swift_regen_1413(a: u64, b: u32) -> u8
{
    (((if (((((((((0x0u32) as u64) << 32) | (((b as u32)) as u64)) as u64)) as u64) == (((a as u64)) as u64))) { ((0x1u32) as u32) } else { ((0x0u32) as u32) })) as u8)
}
