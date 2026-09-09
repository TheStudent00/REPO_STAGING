#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00017__c_op_37.
// The term's layer-5 text, LITERAL:
//   1 + v0
#[no_mangle]
pub extern "C" fn emu_E00017__c_op_37(a: u64) -> u64
{
    ((((((((a as u64)) as u64)).wrapping_add(((0x1u64) as u64))) as u64)) as u64)
}
