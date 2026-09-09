#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o13 emulation WITH THE MODE -- rendered by mode.py
// ModeRendererRust from the layer-4 term of rust__E01540__go_regen_286,
// and from the guard the reference read off the x unit's own body.
// The term's layer-5 text, LITERAL:
//   v1 >> Concat(0, Extract(5, 0, v0) | ~(63*If(Or(Not(Extract(15, 7, v0) == 0), ULE(64, Extract(6, 0, v0))), 0, 1)))
#[no_mangle]
pub extern "C" fn emu_rust__E01540__go_regen_286(a: u64, b: u16, c: u64) -> u64
{
    (((if ((((((((0x0u64) as u64) << 6) | ((((((((((!(((((((((if (((((((0x40u32) as u32)) <= ((((((((b as u32)) >> 0) as u32) & 0x7fu32)) as u32)))) || ((!(((((((((b as u32)) >> 7) as u32) & 0x1ffu32)) as u32) == ((0x0u32) as u32))))))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u32)).wrapping_mul(((0x3fu32) as u32))) as u32) & 0x3fu32)) as u32)) as u32) & 0x3fu32)) as u32) | (((((((b as u32)) >> 0) as u32) & 0x3fu32)) as u32)) as u32) & 0x3fu32)) as u64)) as u64)) as u64) < (0x40u64)) { ((((((a as u64)) as i64)).wrapping_shr(((((((((0x0u64) as u64) << 6) | ((((((((((!(((((((((if (((((((0x40u32) as u32)) <= ((((((((b as u32)) >> 0) as u32) & 0x7fu32)) as u32)))) || ((!(((((((((b as u32)) >> 7) as u32) & 0x1ffu32)) as u32) == ((0x0u32) as u32))))))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u32)).wrapping_mul(((0x3fu32) as u32))) as u32) & 0x3fu32)) as u32)) as u32) & 0x3fu32)) as u32) | (((((((b as u32)) >> 0) as u32) & 0x3fu32)) as u32)) as u32) & 0x3fu32)) as u64)) as u64)) as u64) as u32))) as u64) } else { (if ((((a as u64)) as i64)) < 0 { 0xffffffffffffffffu64 } else { 0 as u64 }) })) as u64)
}
