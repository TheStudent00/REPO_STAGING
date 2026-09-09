#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of sub_cl_gpr_8__flags__rust.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(7, 0, v0), Extract(7, 0, v1))
#[no_mangle]
pub extern "C" fn emu_sub_cl_gpr_8__flags__rust(a: u8, b: u8) -> u16
{
    (((((((((a as u32)) as u32) << 8) | (((b as u32)) as u32)) as u32) & 0xffffu32)) as u16)
}
