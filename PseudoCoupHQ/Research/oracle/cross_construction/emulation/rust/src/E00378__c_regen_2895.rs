#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00378__c_regen_2895.
// The term's layer-5 text, LITERAL:
//   If(0 <= v0, 0, 1)
#[no_mangle]
pub extern "C" fn emu_E00378__c_regen_2895(a: u64) -> u8
{
    (((if (((((0x0u64) as i64)) <= ((((a as u64)) as i64)))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u8)
}
