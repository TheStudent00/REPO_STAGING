#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of opcode_c_64.
// The term's layer-5 text, LITERAL:
//   LShR(v0, Concat(0, Extract(5, 0, v1)))
#[no_mangle]
pub extern "C" fn emu_opcode_c_64(a: u64, b: u8) -> u64
{
    (((((((a as u64)) as u64).wrapping_shr(((((((((0x0u64) as u64) << 6) | (((((((b as u32)) >> 0) as u32) & 0x3fu32)) as u64)) as u64)) as u64) as u32))) as u64)) as u64)
}
