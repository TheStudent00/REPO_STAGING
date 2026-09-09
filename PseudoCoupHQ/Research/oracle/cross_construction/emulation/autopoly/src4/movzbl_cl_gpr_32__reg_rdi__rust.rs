#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of movzbl_cl_gpr_32__reg_rdi__rust.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(7, 0, v0))
#[no_mangle]
pub extern "C" fn emu_movzbl_cl_gpr_32__reg_rdi__rust(a: u8) -> u64
{
    (((((((0x0u64) as u64) << 8) | (((a as u32)) as u64)) as u64)) as u64)
}
