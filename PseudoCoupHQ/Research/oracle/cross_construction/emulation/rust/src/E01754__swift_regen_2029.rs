#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E01754__swift_regen_2029.
// The term's layer-5 text, LITERAL:
//   v1 >> Concat(0, If(Or(Not(Extract(7, 6, v0) == 0), Extract(5, 0, v0) == 63), 63, Extract(5, 0, v0)))
#[no_mangle]
pub extern "C" fn emu_E01754__swift_regen_2029(a: u64, b: u8) -> u64
{
    ((((((((a as u64)) as i64)).wrapping_shr(((((((((0x0u64) as u64) << 6) | (((if (((((((((((b as u32)) >> 0) as u32) & 0x3fu32)) as u32) == ((0x3fu32) as u32))) || ((!(((((((((b as u32)) >> 6) as u32) & 0x3u32)) as u32) == ((0x0u32) as u32))))))) { ((0x3fu32) as u32) } else { (((((((b as u32)) >> 0) as u32) & 0x3fu32)) as u32) })) as u64)) as u64)) as u64) as u32))) as u64)) as u64)
}
