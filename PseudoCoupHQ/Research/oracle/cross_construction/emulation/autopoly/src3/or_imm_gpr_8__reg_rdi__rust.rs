#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of or_imm_gpr_8__reg_rdi__rust.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(7, 2, v0), 3)
#[no_mangle]
pub extern "C" fn emu_or_imm_gpr_8__reg_rdi__rust(a: u8) -> u64
{
    (((((((0x0u64) as u64) << 8) | ((((((((a as u32)) >> 2) as u32) & 0x3fu32)) as u64) << 2) | ((0x3u32) as u64)) as u64)) as u64)
}
