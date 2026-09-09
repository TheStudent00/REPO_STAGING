#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00631__c_regen_19972.
// The term's layer-5 text, LITERAL:
//   Concat(0, ~(If(v0 | v1 == 0, 255, 254) | If(v2 | v3 == 0, 255, 254)))
#[no_mangle]
pub extern "C" fn emu_E00631__c_regen_19972(a: u64, b: u64, c: u64, d: u64) -> u32
{
    (((((((0x0u32) as u32) << 8) | (((((!((((((((if (((((((((d as u64)) as u64) | (((c as u64)) as u64)) as u64)) as u64) == ((0x0u64) as u64))) { ((0xffu32) as u32) } else { ((0xfeu32) as u32) })) as u32) | (((if (((((((((a as u64)) as u64) | (((b as u64)) as u64)) as u64)) as u64) == ((0x0u64) as u64))) { ((0xffu32) as u32) } else { ((0xfeu32) as u32) })) as u32)) as u32) & 0xffu32)) as u32)) as u32) & 0xffu32)) as u32)) as u32)) as u32)
}
