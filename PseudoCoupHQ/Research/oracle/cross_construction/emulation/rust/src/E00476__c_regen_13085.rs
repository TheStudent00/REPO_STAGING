#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00476__c_regen_13085.
// The term's layer-5 text, LITERAL:
//   Extract(63, 0, bvudiv_i(Concat(0, v0), Concat(0, Extract(31, 0, v1))))
#[no_mangle]
pub extern "C" fn emu_E00476__c_regen_13085(a: u64, b: u32, c: u64) -> u64
{
    ((((((((({ let n1: u128 = (((((((0x0u64) as u128) << 64) | (((a as u64)) as u128)) as u128)) as u128); let d1: u128 = (((((((0x0u128) as u128) << 32) | (((b as u32)) as u128)) as u128)) as u128); unsafe { if d1 == 0 { core::hint::unreachable_unchecked(); } } n1 / d1 })) as u128)) as u128) >> 0) as u64)) as u64)
}
