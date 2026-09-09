#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00592__c_regen_18911.
// The term's layer-5 text, LITERAL:
//   Concat(0, ~(~Extract(7, 0, v0) | If(Extract(7, 0, v1) == 0, 255, 254)))
#[no_mangle]
pub extern "C" fn emu_E00592__c_regen_18911(a: u8, b: u8) -> u32
{
    (((((((0x0u32) as u32) << 8) | (((((!((((((((((!(((a as u32)) as u32)) as u32) & 0xffu32)) as u32) | (((if (((((b as u32)) as u32) == ((0x0u32) as u32))) { ((0xffu32) as u32) } else { ((0xfeu32) as u32) })) as u32)) as u32) & 0xffu32)) as u32)) as u32) & 0xffu32)) as u32)) as u32)) as u32)
}
