#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of control__E00211__rust_op_368.
// The term's layer-5 text, LITERAL:
//   If(ULE(v0, v1), 1, 0)
#[no_mangle]
pub extern "C" fn emu_control__E00211__rust_op_368(a: u64, b: u64) -> u8
{
    (((if ((((((a as u64)) as u64)) <= ((((b as u64)) as u64)))) { ((0x1u32) as u32) } else { ((0x0u32) as u32) })) as u8)
}
