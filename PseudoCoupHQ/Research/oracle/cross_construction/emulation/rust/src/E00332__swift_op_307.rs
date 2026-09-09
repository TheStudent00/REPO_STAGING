#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00332__swift_op_307.
// The term's layer-5 text, LITERAL:
//   ~(If(v0 <= 0, 255, 254) | If(ULE(v0, v1), 255, 254))
#[no_mangle]
pub extern "C" fn emu_E00332__swift_op_307(a: u64, b: u64, c: u64) -> u8
{
    (((((!((((((((if ((((((b as u64)) as i64)) <= (((0x0u64) as i64)))) { ((0xffu32) as u32) } else { ((0xfeu32) as u32) })) as u32) | (((if ((((((b as u64)) as u64)) <= ((((a as u64)) as u64)))) { ((0xffu32) as u32) } else { ((0xfeu32) as u32) })) as u32)) as u32) & 0xffu32)) as u32)) as u32) & 0xffu32)) as u8)
}
