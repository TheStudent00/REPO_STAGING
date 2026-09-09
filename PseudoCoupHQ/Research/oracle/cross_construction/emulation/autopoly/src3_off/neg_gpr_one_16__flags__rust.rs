#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of neg_gpr_one_16__flags__rust.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(15, 0, v0), 0)
#[no_mangle]
pub extern "C" fn emu_neg_gpr_one_16__flags__rust(a: u16) -> u32
{
    ((((((((a as u32)) as u32) << 16) | ((0x0u32) as u32)) as u32)) as u32)
}
