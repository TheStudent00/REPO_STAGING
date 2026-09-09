#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o13 emulation WITH THE MODE -- rendered by mode.py
// ModeRendererRust from the layer-4 term of rust__E01536__go_regen_165,
// and from the guard the reference read off the x unit's own body.
// The term's layer-5 text, LITERAL:
//   ~(~(v0 << Concat(0, Extract(5, 0, v1))) | ~(18446744073709551615*If(Or(Not(Extract(15, 7, v1) == 0), ULE(64, Extract(6, 0, v1))), 0, 1)))
#[no_mangle]
pub extern "C" fn emu_rust__E01536__go_regen_165(a: u64, b: u16) -> u64
{
    ((((!((((((((!((((((((if (((((((0x40u32) as u32)) <= ((((((((b as u32)) >> 0) as u32) & 0x7fu32)) as u32)))) || ((!(((((((((b as u32)) >> 7) as u32) & 0x1ffu32)) as u32) == ((0x0u32) as u32))))))) { ((0x0u64) as u64) } else { ((0x1u64) as u64) })) as u64)).wrapping_mul(((0xffffffffffffffffu64) as u64))) as u64)) as u64)) as u64)) as u64) | ((((!(((((((a as u64)) as u64).wrapping_shl(((((((((0x0u64) as u64) << 6) | (((((((b as u32)) >> 0) as u32) & 0x3fu32)) as u64)) as u64)) as u64) as u32))) as u64)) as u64)) as u64)) as u64)) as u64)) as u64)) as u64)) as u64)
}
