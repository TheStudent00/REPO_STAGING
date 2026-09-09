#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
extern "C" { fn runtime_panicdivide() -> !; }

// task o13 emulation WITH THE MODE -- rendered by mode.py
// ModeRendererRust from the layer-4 term of rust__E01532__go_regen_146,
// and from the guard the reference read off the x unit's own body.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(15, 0, bvudiv_i(Concat(0, Extract(7, 0, v0)), Concat(0, Extract(7, 0, v1)))))
#[no_mangle]
pub extern "C" fn emu_rust__E01532__go_regen_146(a: u8, b: u8) -> u32
{
    if ((true) && ((((0x0u32) as u32) == ((((((((b as u32)) as u32) & (((b as u32)) as u32)) as u32) & 0xffu32)) as u32)))) { unsafe { runtime_panicdivide() }; }
    (((((((0x0u32) as u32) << 16) | (((((((((({ let n1: u32 = (((((((0x0u32) as u32) << 8) | (((a as u32)) as u32)) as u32)) as u32); let d1: u32 = (((((((0x0u32) as u32) << 8) | (((b as u32)) as u32)) as u32)) as u32); unsafe { if d1 == 0 { core::hint::unreachable_unchecked(); } } n1 / d1 })) as u32)) as u32) >> 0) as u32) & 0xffffu32)) as u32)) as u32)) as u32)
}
