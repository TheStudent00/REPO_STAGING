#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00032__c_op_113.
// The term's layer-5 text, LITERAL:
//   v0 + Concat(0, Extract(31, 0, v1))
#[no_mangle]
pub extern "C" fn emu_E00032__c_op_113(a: u64, b: u32) -> u64
{
    ((((((((((((0x0u32) as u64) << 32) | (((b as u32)) as u64)) as u64)) as u64)).wrapping_add((((a as u64)) as u64))) as u64)) as u64)
}
