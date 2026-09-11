#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of mov_imm_gpr_16__reg_rdi__rust.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 16, v0), Extract(15, 0, v1))
#[no_mangle]
pub extern "C" fn emu_mov_imm_gpr_16__reg_rdi__rust(a: u64, b: u16) -> u64
{
    ((((((((((((a as u64)) >> 16) as u64) & 0xffffffffffffu64)) as u64) << 16) | (((b as u32)) as u64)) as u64)) as u64)
}
