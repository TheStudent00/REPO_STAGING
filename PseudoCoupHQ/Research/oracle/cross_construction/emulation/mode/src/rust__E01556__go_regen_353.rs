#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o13 emulation WITH THE MODE -- rendered by mode.py
// ModeRendererRust from the layer-4 term of rust__E01556__go_regen_353,
// and from the guard the reference read off the x unit's own body.
// The term's layer-5 text, LITERAL:
//   Concat(0, ~(~LShR(Extract(15, 0, v0), Concat(0, Extract(4, 0, v1))) | ~(65535*If(Or(Not(Extract(31, 5, v1) == 0), ULE(16, Extract(4, 0, v1))), 0, 1))))
#[no_mangle]
pub extern "C" fn emu_rust__E01556__go_regen_353(a: u16, b: u32) -> u32
{
    (((((((0x0u32) as u32) << 16) | (((((!((((((((((!(((if (((((((((0x0u32) as u32) << 5) | (((((((b as u32)) >> 0) as u32) & 0x1fu32)) as u32)) as u32) & 0xffffu32)) as u32) < (0x10u32)) { ((((((a as u32)) as u32).wrapping_shr((((((((((0x0u32) as u32) << 5) | (((((((b as u32)) >> 0) as u32) & 0x1fu32)) as u32)) as u32) & 0xffffu32)) as u32) as u32))) as u32) & 0xffffu32) } else { (0 as u32) })) as u32)) as u32) & 0xffffu32)) as u32) | (((((!(((((((((if (((((((0x10u32) as u32)) <= ((((((((b as u32)) >> 0) as u32) & 0x1fu32)) as u32)))) || ((!(((((((((b as u32)) >> 5) as u32) & 0x7ffffffu32)) as u32) == ((0x0u32) as u32))))))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u32)).wrapping_mul(((0xffffu32) as u32))) as u32) & 0xffffu32)) as u32)) as u32) & 0xffffu32)) as u32)) as u32) & 0xffffu32)) as u32)) as u32) & 0xffffu32)) as u32)) as u32)) as u32)
}
