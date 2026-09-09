#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E01780__swift_regen_2084.
// The term's layer-5 text, LITERAL:
//   Extract(7, 0, v1) >> Concat(0, If(Or(Not(Extract(63, 3, v0) == 0), Extract(2, 0, v0) == 7), 7, Extract(4, 0, v0)))
#[no_mangle]
pub extern "C" fn emu_E01780__swift_regen_2084(a: u8, b: u64) -> u8
{
    (((if (((((((((0x0u32) as u32) << 5) | (((if (((((((((((b as u64)) >> 0) as u32) & 0x7u32)) as u32) == ((0x7u32) as u32))) || ((!(((((((((b as u64)) >> 3) as u64) & 0x1fffffffffffffffu64)) as u64) == ((0x0u64) as u64))))))) { ((0x7u32) as u32) } else { (((((((b as u64)) >> 0) as u32) & 0x1fu32)) as u32) })) as u32)) as u32) & 0xffu32)) as u32) < (0x8u32)) { ((((((((((a as u32)) as u32) << 24) as i32) >> 24)).wrapping_shr((((((((((0x0u32) as u32) << 5) | (((if (((((((((((b as u64)) >> 0) as u32) & 0x7u32)) as u32) == ((0x7u32) as u32))) || ((!(((((((((b as u64)) >> 3) as u64) & 0x1fffffffffffffffu64)) as u64) == ((0x0u64) as u64))))))) { ((0x7u32) as u32) } else { (((((((b as u64)) >> 0) as u32) & 0x1fu32)) as u32) })) as u32)) as u32) & 0xffu32)) as u32) as u32))) as u32) & 0xffu32) } else { (if (((((((a as u32)) as u32) << 24) as i32) >> 24)) < 0 { 0xffu32 } else { 0 as u32 }) })) as u8)
}
