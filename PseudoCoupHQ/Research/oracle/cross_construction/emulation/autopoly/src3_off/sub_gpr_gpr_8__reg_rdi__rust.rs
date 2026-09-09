#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of sub_gpr_gpr_8__reg_rdi__rust.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(7, 0, v0)*255 + Extract(7, 0, v1))
#[no_mangle]
pub extern "C" fn emu_sub_gpr_gpr_8__reg_rdi__rust(a: u8, b: u8) -> u64
{
    (((((((0x0u64) as u64) << 8) | (((((((((((((((b as u32)) as u32)).wrapping_mul(((0xffu32) as u32))) as u32) & 0xffu32)) as u32)).wrapping_add((((a as u32)) as u32))) as u32) & 0xffu32)) as u64)) as u64)) as u64)
}
