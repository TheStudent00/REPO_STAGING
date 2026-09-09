#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E01791__swift_regen_2098.
// The term's layer-5 text, LITERAL:
//   If(Or(Not(Extract(15, 7, v0) == 0), ULE(64, Extract(6, 0, v0))), 0, LShR(v1, Concat(0, Extract(5, 0, v0))))
#[no_mangle]
pub extern "C" fn emu_E01791__swift_regen_2098(a: u64, b: u16) -> u64
{
    (((if (((((((0x40u32) as u32)) <= ((((((((b as u32)) >> 0) as u32) & 0x7fu32)) as u32)))) || ((!(((((((((b as u32)) >> 7) as u32) & 0x1ffu32)) as u32) == ((0x0u32) as u32))))))) { ((0x0u64) as u64) } else { (((((((a as u64)) as u64).wrapping_shr(((((((((0x0u64) as u64) << 6) | (((((((b as u32)) >> 0) as u32) & 0x3fu32)) as u64)) as u64)) as u64) as u32))) as u64)) as u64) })) as u64)
}
