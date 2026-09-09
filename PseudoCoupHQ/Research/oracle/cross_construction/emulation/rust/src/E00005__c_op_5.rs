#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00005__c_op_5.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(7, 1, v0), ~Extract(0, 0, v0))
#[no_mangle]
pub extern "C" fn emu_E00005__c_op_5(a: u8) -> u32
{
    (((((((0x0u32) as u32) << 8) | ((((((((a as u32)) >> 1) as u32) & 0x7fu32)) as u32) << 1) | (((((!(((((((a as u32)) >> 0) as u32) & 0x1u32)) as u32)) as u32) & 0x1u32)) as u32)) as u32)) as u32)
}
