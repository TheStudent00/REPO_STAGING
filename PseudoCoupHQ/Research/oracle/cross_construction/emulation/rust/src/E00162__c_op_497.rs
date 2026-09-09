#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00162__c_op_497.
// The term's layer-5 text, LITERAL:
//   Concat(0, 1 ^ Extract(7, 0, v0) ^ Extract(7, 0, v1))
#[no_mangle]
pub extern "C" fn emu_E00162__c_op_497(a: u8, b: u8) -> u32
{
    (((((((0x0u32) as u32) << 8) | ((((((((a as u32)) as u32) ^ (((b as u32)) as u32) ^ ((0x1u32) as u32)) as u32) & 0xffu32)) as u32)) as u32)) as u32)
}
