#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of add_gpr_gpr_16__reg_rdi__rust.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(15, 0, v0) + Extract(15, 0, v1))
#[no_mangle]
pub extern "C" fn emu_add_gpr_gpr_16__reg_rdi__rust(a: u16, b: u16) -> u64
{
    (((((((0x0u64) as u64) << 16) | (((((((((a as u32)) as u32)).wrapping_add((((b as u32)) as u32))) as u32) & 0xffffu32)) as u64)) as u64)) as u64)
}
