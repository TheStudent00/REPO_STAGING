#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of pextrw_imm_xmm_gpr_128__reg_rdi__rust.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(31, 16, v0))
#[no_mangle]
pub extern "C" fn emu_pextrw_imm_xmm_gpr_128__reg_rdi__rust(a: f32) -> u64
{
    (((((((0x0u64) as u64) << 16) | ((((((((a).to_bits() as u32)) >> 16) as u32) & 0xffffu32)) as u64)) as u64)) as u64)
}
