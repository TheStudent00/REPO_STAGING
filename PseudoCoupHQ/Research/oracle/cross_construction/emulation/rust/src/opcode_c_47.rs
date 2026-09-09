#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of opcode_c_47.
// The term's layer-5 text, LITERAL:
//   v0*18446744073709551615
#[no_mangle]
pub extern "C" fn emu_opcode_c_47(a: u64) -> u64
{
    ((((((((a as u64)) as u64)).wrapping_mul(((0xffffffffffffffffu64) as u64))) as u64)) as u64)
}
