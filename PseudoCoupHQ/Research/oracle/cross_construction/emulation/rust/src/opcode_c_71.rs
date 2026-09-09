#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of opcode_c_71.
// The term's layer-5 text, LITERAL:
//   v0*18446744073709551615 + Concat(0, Extract(31, 0, v1))
#[no_mangle]
pub extern "C" fn emu_opcode_c_71(a: u32, b: u64) -> u64
{
    (((((((((((((b as u64)) as u64)).wrapping_mul(((0xffffffffffffffffu64) as u64))) as u64)) as u64)).wrapping_add((((((((0x0u32) as u64) << 32) | (((a as u32)) as u64)) as u64)) as u64))) as u64)) as u64)
}
