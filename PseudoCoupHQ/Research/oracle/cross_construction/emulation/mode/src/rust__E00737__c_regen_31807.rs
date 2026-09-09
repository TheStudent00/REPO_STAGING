#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o13 emulation WITH THE MODE -- rendered by mode.py
// ModeRendererRust from the layer-4 term of rust__E00737__c_regen_31807,
// and from the guard the reference read off the x unit's own body.
// The term's layer-5 text, LITERAL:
//   If(And(Extract(31, 0, v0) | Extract(31, 0, v1) ^ Extract(31, 0, v2) == 0, Extract(63, 32, v0) | Extract(63, 32, v2) == 0), 0, 1)
#[no_mangle]
pub extern "C" fn emu_rust__E00737__c_regen_31807(a: u32, b: u64, c: u64) -> u8
{
    (((if (((((((((((((((a as u32)) as u32) ^ ((((((b as u64)) >> 0) as u32)) as u32)) as u32)) as u32) | ((((((c as u64)) >> 0) as u32)) as u32)) as u32)) as u32) == ((0x0u32) as u32))) && ((((((((((((c as u64)) >> 32) as u32)) as u32) | ((((((b as u64)) >> 32) as u32)) as u32)) as u32)) as u32) == ((0x0u32) as u32))))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u8)
}
