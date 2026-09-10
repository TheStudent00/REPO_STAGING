#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of div_gpr_one_8__reg_rax__rust.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 16, v0), Extract(7, 0, bvurem_i(Extract(15, 0, v0), Concat(0, Extract(7, 0, v1)))), Extract(7, 0, bvudiv_i(Extract(15, 0, v0), Concat(0, Extract(7, 0, v1)))))
#[no_mangle]
pub extern "C" fn emu_div_gpr_one_8__reg_rax__rust(a: u64, b: u8) -> u64
{
    ((((((((((((a as u64)) >> 16) as u64) & 0xffffffffffffu64)) as u64) << 16) | (((((((((((({ let n1: u32 = (((((((a as u64)) >> 0) as u32) & 0xffffu32)) as u32); let d1: u32 = ((((((((0x0u32) as u32) << 8) | (((b as u32)) as u32)) as u32) & 0xffffu32)) as u32); unsafe { if d1 == 0 { core::hint::unreachable_unchecked(); } } n1 % d1 })) as u32) & 0xffffu32)) as u32) >> 0) as u32) & 0xffu32)) as u64) << 8) | ((((((((((({ let n2: u32 = (((((((a as u64)) >> 0) as u32) & 0xffffu32)) as u32); let d2: u32 = ((((((((0x0u32) as u32) << 8) | (((b as u32)) as u32)) as u32) & 0xffffu32)) as u32); unsafe { if d2 == 0 { core::hint::unreachable_unchecked(); } } n2 / d2 })) as u32) & 0xffffu32)) as u32) >> 0) as u32) & 0xffu32)) as u64)) as u64)) as u64)
}
