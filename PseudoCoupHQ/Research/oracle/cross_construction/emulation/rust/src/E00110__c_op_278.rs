#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00110__c_op_278.
// The term's layer-5 text, LITERAL:
//   Extract(63, 0, bvurem_i(Concat(0, Extract(31, 0, v0)), Concat(0, v1)))
#[no_mangle]
pub extern "C" fn emu_E00110__c_op_278(a: u32, b: u64, c: u64) -> u64
{
    ((((((((({ let n1: u128 = (((((((0x0u128) as u128) << 32) | (((a as u32)) as u128)) as u128)) as u128); let d1: u128 = (((((((0x0u64) as u128) << 64) | (((b as u64)) as u128)) as u128)) as u128); unsafe { if d1 == 0 { core::hint::unreachable_unchecked(); } } n1 % d1 })) as u128)) as u128) >> 0) as u64)) as u64)
}
