#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E01723__swift_regen_1966.
// The term's layer-5 text, LITERAL:
//   If(Or(ULE(128, Extract(7, 0, v0)), Not(Extract(15, 8, v0) == 0), Not(Extract(6, 6, v0) == 0)), 0, v1 << Concat(0, Extract(5, 0, v0)))
#[no_mangle]
pub extern "C" fn emu_E01723__swift_regen_1966(a: u64, b: u64, c: u16) -> u64
{
    (((if (((((((0x80u32) as u32)) <= ((((((((c as u32)) >> 0) as u32) & 0xffu32)) as u32)))) || ((!(((((((((c as u32)) >> 8) as u32) & 0xffu32)) as u32) == ((0x0u32) as u32))))) || ((!(((((((((c as u32)) >> 6) as u32) & 0x1u32)) as u32) == ((0x0u32) as u32))))))) { ((0x0u64) as u64) } else { (((((((a as u64)) as u64).wrapping_shl(((((((((0x0u64) as u64) << 6) | (((((((c as u32)) >> 0) as u32) & 0x3fu32)) as u64)) as u64)) as u64) as u32))) as u64)) as u64) })) as u64)
}
