#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of shr_imm_gpr_64__reg_rdi__rust.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(63, 3, v0))
#[no_mangle]
pub extern "C" fn emu_shr_imm_gpr_64__reg_rdi__rust(a: u64) -> u64
{
    (((((((0x0u32) as u64) << 61) | (((((((a as u64)) >> 3) as u64) & 0x1fffffffffffffffu64)) as u64)) as u64)) as u64)
}
