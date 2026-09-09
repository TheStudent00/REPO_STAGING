#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o13 emulation WITH THE MODE -- rendered by mode.py
// ModeRendererRust from the layer-4 term of rust__E01771__swift_regen_2049,
// and from the guard the reference read off the x unit's own body.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 0, v0)) >> 15
#[no_mangle]
pub extern "C" fn emu_rust__E01771__swift_regen_2049(a: u16, b: u64, c: u64) -> u32
{
    (((((((((((((((((a as u32)) >> 15) as u32) & 0x1u32)) as u32) << 31) | ((((((((a as u32)) >> 15) as u32) & 0x1u32)) as u32) << 30) | ((((((((a as u32)) >> 15) as u32) & 0x1u32)) as u32) << 29) | ((((((((a as u32)) >> 15) as u32) & 0x1u32)) as u32) << 28) | ((((((((a as u32)) >> 15) as u32) & 0x1u32)) as u32) << 27) | ((((((((a as u32)) >> 15) as u32) & 0x1u32)) as u32) << 26) | ((((((((a as u32)) >> 15) as u32) & 0x1u32)) as u32) << 25) | ((((((((a as u32)) >> 15) as u32) & 0x1u32)) as u32) << 24) | ((((((((a as u32)) >> 15) as u32) & 0x1u32)) as u32) << 23) | ((((((((a as u32)) >> 15) as u32) & 0x1u32)) as u32) << 22) | ((((((((a as u32)) >> 15) as u32) & 0x1u32)) as u32) << 21) | ((((((((a as u32)) >> 15) as u32) & 0x1u32)) as u32) << 20) | ((((((((a as u32)) >> 15) as u32) & 0x1u32)) as u32) << 19) | ((((((((a as u32)) >> 15) as u32) & 0x1u32)) as u32) << 18) | ((((((((a as u32)) >> 15) as u32) & 0x1u32)) as u32) << 17) | ((((((((a as u32)) >> 15) as u32) & 0x1u32)) as u32) << 16) | (((a as u32)) as u32)) as u32)) as i32)).wrapping_shr((((0xfu32) as u32) as u32))) as u32)) as u32)
}
