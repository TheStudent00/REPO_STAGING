#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E01781__swift_regen_2085.
// The term's layer-5 text, LITERAL:
//   Extract(7, 0, v0) >> 7
#[no_mangle]
pub extern "C" fn emu_E01781__swift_regen_2085(a: u8, b: u64, c: u64) -> u8
{
    ((((((((((((a as u32)) as u32) << 24) as i32) >> 24)).wrapping_shr((((0x7u32) as u32) as u32))) as u32) & 0xffu32)) as u8)
}
