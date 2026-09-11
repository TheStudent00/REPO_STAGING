#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of not_gpr_one_8__reg_rdi__rust.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 8, v0), ~Extract(7, 0, v0))
#[no_mangle]
pub extern "C" fn emu_not_gpr_one_8__reg_rdi__rust(a: u64) -> u64
{
    ((((((((((((a as u64)) >> 8) as u64) & 0xffffffffffffffu64)) as u64) << 8) | (((((!(((((((a as u64)) >> 0) as u32) & 0xffu32)) as u32)) as u32) & 0xffu32)) as u64)) as u64)) as u64)
}
