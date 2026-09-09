#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of opcode_c_54.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 32, v0), Extract(31, 0, v0) | Extract(31, 0, v1))
#[no_mangle]
pub extern "C" fn emu_opcode_c_54(a: u64, b: u64, c: u32) -> u64
{
    (((((((((((a as u64)) >> 32) as u32)) as u64) << 32) | ((((((((((a as u64)) >> 0) as u32)) as u32) | (((c as u32)) as u32)) as u32)) as u64)) as u64)) as u64)
}
