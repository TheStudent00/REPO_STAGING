#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00557__c_regen_17015.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(v0 == 0, 0, 1) | If(Extract(7, 0, v1) == 0, 0, 1))
#[no_mangle]
pub extern "C" fn emu_E00557__c_regen_17015(a: u8, b: u64, c: u64) -> u32
{
    (((((((0x0u32) as u32) << 8) | ((((((((if (((((a as u32)) as u32) == ((0x0u32) as u32))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u32) | (((if (((((b as u64)) as u64) == ((0x0u64) as u64))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u32)) as u32) & 0xffu32)) as u32)) as u32)) as u32)
}
