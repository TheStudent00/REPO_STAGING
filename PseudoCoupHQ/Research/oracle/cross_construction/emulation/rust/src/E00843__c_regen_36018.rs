#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00843__c_regen_36018.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(v0 <= v1 >> 63, 0, 1))
#[no_mangle]
pub extern "C" fn emu_E00843__c_regen_36018(a: u64, b: u64, c: u64) -> u32
{
    (((((((0x0u32) as u32) << 8) | (((if ((((((b as u64)) as i64)) <= (((((((((c as u64)) as i64)).wrapping_shr((((0x3fu64) as u64) as u32))) as u64)) as i64)))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u32)) as u32)) as u32)
}
