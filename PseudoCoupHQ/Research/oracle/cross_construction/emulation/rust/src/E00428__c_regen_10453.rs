#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00428__c_regen_10453.
// The term's layer-5 text, LITERAL:
//   Extract(31, 0, bvudiv_i(Concat(0, Extract(31, 0, v0)), Concat(0, Extract(31, 0, v1))))
#[no_mangle]
pub extern "C" fn emu_E00428__c_regen_10453(a: u32, b: u32, c: u64) -> u32
{
    ((((((((({ let n1: u64 = (((((((0x0u32) as u64) << 32) | (((a as u32)) as u64)) as u64)) as u64); let d1: u64 = (((((((0x0u32) as u64) << 32) | (((b as u32)) as u64)) as u64)) as u64); unsafe { if d1 == 0 { core::hint::unreachable_unchecked(); } } n1 / d1 })) as u64)) as u64) >> 0) as u32)) as u32)
}
