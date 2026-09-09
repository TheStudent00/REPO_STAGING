#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E01710__swift_regen_1943.
// The term's layer-5 text, LITERAL:
//   If(Or(Not(Extract(31, 4, v0) == 0), ULE(8, Extract(3, 0, v0))), 0, Concat(0, Extract(7, 0, v1) << Concat(0, Extract(2, 0, v0))))
#[no_mangle]
pub extern "C" fn emu_E01710__swift_regen_1943(a: u8, b: u32) -> u32
{
    (((if (((((((0x8u32) as u32)) <= ((((((((b as u32)) >> 0) as u32) & 0xfu32)) as u32)))) || ((!(((((((((b as u32)) >> 4) as u32) & 0xfffffffu32)) as u32) == ((0x0u32) as u32))))))) { ((0x0u32) as u32) } else { (((((((0x0u32) as u32) << 8) | ((((((((a as u32)) as u32).wrapping_shl((((((((((0x0u32) as u32) << 3) | (((((((b as u32)) >> 0) as u32) & 0x7u32)) as u32)) as u32) & 0xffu32)) as u32) as u32))) as u32) & 0xffu32)) as u32)) as u32)) as u32) })) as u32)
}
