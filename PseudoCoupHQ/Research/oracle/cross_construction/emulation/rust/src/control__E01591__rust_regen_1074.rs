#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of control__E01591__rust_regen_1074.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(31, 16, v0), Extract(15, 0, bvudiv_i(Concat(0, Extract(15, 0, v0)), Concat(0, Extract(15, 0, v1)))))
#[no_mangle]
pub extern "C" fn emu_control__E01591__rust_regen_1074(a: u32, b: u16, c: u64) -> u64
{
    (((((((0x0u32) as u64) << 32) | ((((((((a as u32)) >> 16) as u32) & 0xffffu32)) as u64) << 16) | (((((((((({ let n1: u32 = (((((((0x0u32) as u32) << 16) | (((((((a as u32)) >> 0) as u32) & 0xffffu32)) as u32)) as u32)) as u32); let d1: u32 = (((((((0x0u32) as u32) << 16) | (((b as u32)) as u32)) as u32)) as u32); unsafe { if d1 == 0 { core::hint::unreachable_unchecked(); } } n1 / d1 })) as u32)) as u32) >> 0) as u32) & 0xffffu32)) as u64)) as u64)) as u64)
}
