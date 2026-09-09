#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of opcode_c_66.
// The term's layer-5 text, LITERAL:
//   LShR(Extract(31, 0, v0), Concat(0, Extract(4, 0, v1)))
#[no_mangle]
pub extern "C" fn emu_opcode_c_66(a: u32, b: u8) -> u32
{
    (((((((a as u32)) as u32).wrapping_shr(((((((((0x0u32) as u32) << 5) | (((((((b as u32)) >> 0) as u32) & 0x1fu32)) as u32)) as u32)) as u32) as u32))) as u32)) as u32)
}
