#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E01549__go_regen_330.
// The term's layer-5 text, LITERAL:
//   Extract(7, 0, v1) >> Concat(0, Extract(4, 0, v0) | ~(31*If(Or(Not(Extract(15, 4, v0) == 0), ULE(8, Extract(3, 0, v0))), 0, 1)))
#[no_mangle]
pub extern "C" fn emu_E01549__go_regen_330(a: u8, b: u16, c: u64) -> u8
{
    (((if (((((((((0x0u32) as u32) << 5) | ((((((((((!(((((((((if (((((((0x8u32) as u32)) <= ((((((((b as u32)) >> 0) as u32) & 0xfu32)) as u32)))) || ((!(((((((((b as u32)) >> 4) as u32) & 0xfffu32)) as u32) == ((0x0u32) as u32))))))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u32)).wrapping_mul(((0x1fu32) as u32))) as u32) & 0x1fu32)) as u32)) as u32) & 0x1fu32)) as u32) | (((((((b as u32)) >> 0) as u32) & 0x1fu32)) as u32)) as u32) & 0x1fu32)) as u32)) as u32) & 0xffu32)) as u32) < (0x8u32)) { ((((((((((a as u32)) as u32) << 24) as i32) >> 24)).wrapping_shr((((((((((0x0u32) as u32) << 5) | ((((((((((!(((((((((if (((((((0x8u32) as u32)) <= ((((((((b as u32)) >> 0) as u32) & 0xfu32)) as u32)))) || ((!(((((((((b as u32)) >> 4) as u32) & 0xfffu32)) as u32) == ((0x0u32) as u32))))))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u32)).wrapping_mul(((0x1fu32) as u32))) as u32) & 0x1fu32)) as u32)) as u32) & 0x1fu32)) as u32) | (((((((b as u32)) >> 0) as u32) & 0x1fu32)) as u32)) as u32) & 0x1fu32)) as u32)) as u32) & 0xffu32)) as u32) as u32))) as u32) & 0xffu32) } else { (if (((((((a as u32)) as u32) << 24) as i32) >> 24)) < 0 { 0xffu32 } else { 0 as u32 }) })) as u8)
}
