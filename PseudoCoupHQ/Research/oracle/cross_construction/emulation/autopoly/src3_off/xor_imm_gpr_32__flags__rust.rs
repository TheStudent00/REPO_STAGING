#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of xor_imm_gpr_32__flags__rust.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(31, 2, v0), ~Extract(1, 0, v0), 0)
#[no_mangle]
pub extern "C" fn emu_xor_imm_gpr_32__flags__rust(a: u32) -> u64
{
    ((((((((((((a as u32)) >> 2) as u32) & 0x3fffffffu32)) as u64) << 34) | ((((((!(((((((a as u32)) >> 0) as u32) & 0x3u32)) as u32)) as u32) & 0x3u32)) as u64) << 32) | ((0x0u32) as u64)) as u64)) as u64)
}
