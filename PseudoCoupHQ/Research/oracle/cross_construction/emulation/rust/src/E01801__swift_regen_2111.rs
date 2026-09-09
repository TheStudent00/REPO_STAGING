#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E01801__swift_regen_2111.
// The term's layer-5 text, LITERAL:
//   If(Or(Not(Extract(31, 8, v0) == 0), ULE(128, Extract(7, 0, v0))), 0, If(Extract(6, 6, v0) == 0, Extract(63, 0, LShR(Concat(v1, v2), Concat(0, Extract(5, 0, v0)))), LShR(v1, Concat(0, Extract(5, 0, v0)))))
#[no_mangle]
pub extern "C" fn emu_E01801__swift_regen_2111(a: u64, b: u64, c: u32) -> u64
{
    (((if (((((((0x80u32) as u32)) <= ((((((((c as u32)) >> 0) as u32) & 0xffu32)) as u32)))) || ((!(((((((((c as u32)) >> 8) as u32) & 0xffffffu32)) as u32) == ((0x0u32) as u32))))))) { ((0x0u64) as u64) } else { (((if (((((((((c as u32)) >> 6) as u32) & 0x1u32)) as u32) == ((0x0u32) as u32))) { ((((((((((((((((b as u64)) as u128) << 64) | (((a as u64)) as u128)) as u128)) as u128).wrapping_shr(((((((((0x0u128) as u128) << 6) | (((((((c as u32)) >> 0) as u32) & 0x3fu32)) as u128)) as u128)) as u128) as u32))) as u128)) as u128) >> 0) as u64)) as u64) } else { (((((((b as u64)) as u64).wrapping_shr(((((((((0x0u64) as u64) << 6) | (((((((c as u32)) >> 0) as u32) & 0x3fu32)) as u64)) as u64)) as u64) as u32))) as u64)) as u64) })) as u64) })) as u64)
}
