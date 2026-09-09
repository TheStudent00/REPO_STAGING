#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00066__c_op_185.
// The term's layer-5 text, LITERAL:
//   If(Extract(31, 0, v0) == 0, 0, v1)
#[no_mangle]
pub extern "C" fn emu_E00066__c_op_185(a: u64, b: u32) -> u64
{
    (((if (((((b as u32)) as u32) == ((0x0u32) as u32))) { ((0x0u64) as u64) } else { (((a as u64)) as u64) })) as u64)
}
