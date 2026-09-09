#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of control__E00183__rust_op_332.
// The term's layer-5 text, LITERAL:
//   If(ULE(v0, v1), 0, 1)
#[no_mangle]
pub extern "C" fn emu_control__E00183__rust_op_332(a: u64, b: u64) -> u8
{
    (((if ((((((b as u64)) as u64)) <= ((((a as u64)) as u64)))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u8)
}
