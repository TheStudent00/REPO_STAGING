#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E01539__go_regen_179.
// The term's layer-5 text, LITERAL:
//   ~(~(Extract(31, 0, v0) << Concat(0, Extract(4, 0, v1))) | ~(4294967295*If(Or(Not(Extract(7, 6, v1) == 0), ULE(32, Extract(5, 0, v1))), 0, 1)))
#[no_mangle]
pub extern "C" fn emu_E01539__go_regen_179(a: u32, b: u8) -> u32
{
    ((((!((((((((!((((((((if (((((((0x20u32) as u32)) <= ((((((((b as u32)) >> 0) as u32) & 0x3fu32)) as u32)))) || ((!(((((((((b as u32)) >> 6) as u32) & 0x3u32)) as u32) == ((0x0u32) as u32))))))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u32)).wrapping_mul(((0xffffffffu32) as u32))) as u32)) as u32)) as u32)) as u32) | ((((!(((((((a as u32)) as u32).wrapping_shl(((((((((0x0u32) as u32) << 5) | (((((((b as u32)) >> 0) as u32) & 0x1fu32)) as u32)) as u32)) as u32) as u32))) as u32)) as u32)) as u32)) as u32)) as u32)) as u32)) as u32)) as u32)
}
