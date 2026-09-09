#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00548__c_regen_16847.
// The term's layer-5 text, LITERAL:
//   If(v0 | v1 | v2 == 0, 0, 1)
#[no_mangle]
pub extern "C" fn emu_E00548__c_regen_16847(a: u64, b: u64, c: u64) -> u8
{
    (((if (((((((((a as u64)) as u64) | (((c as u64)) as u64) | (((b as u64)) as u64)) as u64)) as u64) == ((0x0u64) as u64))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u8)
}
