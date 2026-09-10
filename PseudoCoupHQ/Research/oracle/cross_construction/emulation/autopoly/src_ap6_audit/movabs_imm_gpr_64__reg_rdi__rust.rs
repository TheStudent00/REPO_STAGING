#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of movabs_imm_gpr_64__reg_rdi__rust.
// The term's layer-5 text, LITERAL:
//   v0
#[no_mangle]
pub extern "C" fn emu_movabs_imm_gpr_64__reg_rdi__rust(a: u64) -> u64
{
    (((a as u64)) as u64)
}
