#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of and_imm_gpr_32__flags__rust.
// The term's layer-5 text, LITERAL:
//   Concat(~(~Extract(31, 0, v0) | ~Extract(31, 0, v1)), 0)
#[no_mangle]
pub extern "C" fn emu_and_imm_gpr_32__flags__rust(a: u32, b: u32) -> u64
{
    (((((((((!((((((((!(((b as u32)) as u32)) as u32)) as u32) | ((((!(((a as u32)) as u32)) as u32)) as u32)) as u32)) as u32)) as u32)) as u64) << 32) | ((0x0u32) as u64)) as u64)) as u64)
}
