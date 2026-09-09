#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of mov_imm_gpr_16__reg_rdi__rust.
// The term's layer-5 text, LITERAL:
//   3
#[no_mangle]
pub extern "C" fn emu_mov_imm_gpr_16__reg_rdi__rust() -> u64
{
    ((0x3u64) as u64)
}
