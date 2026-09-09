#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00016__c_op_36.
// The term's layer-5 text, LITERAL:
//   1 + Extract(31, 0, v0)
#[no_mangle]
pub extern "C" fn emu_E00016__c_op_36(a: u32) -> u32
{
    ((((((((a as u32)) as u32)).wrapping_add(((0x1u32) as u32))) as u32)) as u32)
}
