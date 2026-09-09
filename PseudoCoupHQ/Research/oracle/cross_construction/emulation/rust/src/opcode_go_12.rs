#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of opcode_go_12.
// The term's layer-5 text, LITERAL:
//   Extract(31, 0, v0)*4294967295
#[no_mangle]
pub extern "C" fn emu_opcode_go_12(a: u32) -> u32
{
    ((((((((a as u32)) as u32)).wrapping_mul(((0xffffffffu32) as u32))) as u32)) as u32)
}
