#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00469__c_regen_12973.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(7, 0, bvudiv_i(Concat(0, Extract(7, 0, v0)), Concat(0, Extract(7, 0, v1)))))
#[no_mangle]
pub extern "C" fn emu_E00469__c_regen_12973(a: u8, b: u8) -> u32
{
    (((((((0x0u32) as u32) << 8) | ((((((((((({ let n1: u32 = ((((((((0x0u32) as u32) << 8) | (((a as u32)) as u32)) as u32) & 0xffffu32)) as u32); let d1: u32 = ((((((((0x0u32) as u32) << 8) | (((b as u32)) as u32)) as u32) & 0xffffu32)) as u32); unsafe { if d1 == 0 { core::hint::unreachable_unchecked(); } } n1 / d1 })) as u32) & 0xffffu32)) as u32) >> 0) as u32) & 0xffu32)) as u32)) as u32)) as u32)
}
