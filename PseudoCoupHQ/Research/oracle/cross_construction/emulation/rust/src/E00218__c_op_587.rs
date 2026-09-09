#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00218__c_op_587.
// The term's layer-5 text, LITERAL:
//   If(Or(Not(Extract(63, 32, v0) == 0), ULE(Extract(31, 0, v1), Extract(31, 0, v0))), 1, 0)
#[no_mangle]
pub extern "C" fn emu_E00218__c_op_587(a: u64, b: u32) -> u8
{
    (((if ((((((((b as u32)) as u32)) <= (((((((a as u64)) >> 0) as u32)) as u32)))) || ((!((((((((a as u64)) >> 32) as u32)) as u32) == ((0x0u32) as u32))))))) { ((0x1u32) as u32) } else { ((0x0u32) as u32) })) as u8)
}
