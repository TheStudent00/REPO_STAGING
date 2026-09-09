#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E01809__swift_regen_2122.
// The term's layer-5 text, LITERAL:
//   If(Or(Not(Extract(15, 5, v0) == 0), ULE(16, Extract(4, 0, v0))), 0, LShR(Concat(0, Extract(15, 0, v1)), Concat(0, Extract(3, 0, v0))))
#[no_mangle]
pub extern "C" fn emu_E01809__swift_regen_2122(a: u16, b: u16) -> u32
{
    (((if (((((((0x10u32) as u32)) <= ((((((((b as u32)) >> 0) as u32) & 0x1fu32)) as u32)))) || ((!(((((((((b as u32)) >> 5) as u32) & 0x7ffu32)) as u32) == ((0x0u32) as u32))))))) { ((0x0u32) as u32) } else { (((((((((((0x0u32) as u32) << 16) | (((a as u32)) as u32)) as u32)) as u32).wrapping_shr(((((((((0x0u32) as u32) << 4) | (((((((b as u32)) >> 0) as u32) & 0xfu32)) as u32)) as u32)) as u32) as u32))) as u32)) as u32) })) as u32)
}
