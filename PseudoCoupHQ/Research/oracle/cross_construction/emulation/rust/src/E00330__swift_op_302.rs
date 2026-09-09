#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00330__swift_op_302.
// The term's layer-5 text, LITERAL:
//   If(0 <= v0, 0, 1) | If(ULE(v1, v0), 0, 1)
#[no_mangle]
pub extern "C" fn emu_E00330__swift_op_302(a: u64, b: u64, c: u64) -> u8
{
    ((((((((if (((((0x0u64) as i64)) <= ((((a as u64)) as i64)))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u32) | (((if ((((((b as u64)) as u64)) <= ((((a as u64)) as u64)))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u32)) as u32) & 0xffu32)) as u8)
}
