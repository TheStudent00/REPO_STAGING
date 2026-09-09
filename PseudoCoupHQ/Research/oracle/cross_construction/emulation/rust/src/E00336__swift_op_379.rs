#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00336__swift_op_379.
// The term's layer-5 text, LITERAL:
//   ~(If(0 <= v0, 254, 255) | If(ULE(v1, v0), 254, 255))
#[no_mangle]
pub extern "C" fn emu_E00336__swift_op_379(a: u64, b: u64, c: u64) -> u8
{
    (((((!((((((((if (((((0x0u64) as i64)) <= ((((b as u64)) as i64)))) { ((0xfeu32) as u32) } else { ((0xffu32) as u32) })) as u32) | (((if ((((((a as u64)) as u64)) <= ((((b as u64)) as u64)))) { ((0xfeu32) as u32) } else { ((0xffu32) as u32) })) as u32)) as u32) & 0xffu32)) as u32)) as u32) & 0xffu32)) as u8)
}
