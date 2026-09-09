#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E01544__go_regen_298.
// The term's layer-5 text, LITERAL:
//   Extract(15, 0, v1) >> Concat(0, Extract(4, 0, v0) | ~(31*If(Or(Not(Extract(31, 5, v0) == 0), ULE(16, Extract(4, 0, v0))), 0, 1)))
#[no_mangle]
pub extern "C" fn emu_E01544__go_regen_298(a: u16, b: u32, c: u64) -> u16
{
    (((if (((((((((0x0u32) as u32) << 5) | ((((((((((!(((((((((if (((((((0x10u32) as u32)) <= ((((((((b as u32)) >> 0) as u32) & 0x1fu32)) as u32)))) || ((!(((((((((b as u32)) >> 5) as u32) & 0x7ffffffu32)) as u32) == ((0x0u32) as u32))))))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u32)).wrapping_mul(((0x1fu32) as u32))) as u32) & 0x1fu32)) as u32)) as u32) & 0x1fu32)) as u32) | (((((((b as u32)) >> 0) as u32) & 0x1fu32)) as u32)) as u32) & 0x1fu32)) as u32)) as u32) & 0xffffu32)) as u32) < (0x10u32)) { ((((((((((a as u32)) as u32) << 16) as i32) >> 16)).wrapping_shr((((((((((0x0u32) as u32) << 5) | ((((((((((!(((((((((if (((((((0x10u32) as u32)) <= ((((((((b as u32)) >> 0) as u32) & 0x1fu32)) as u32)))) || ((!(((((((((b as u32)) >> 5) as u32) & 0x7ffffffu32)) as u32) == ((0x0u32) as u32))))))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u32)).wrapping_mul(((0x1fu32) as u32))) as u32) & 0x1fu32)) as u32)) as u32) & 0x1fu32)) as u32) | (((((((b as u32)) >> 0) as u32) & 0x1fu32)) as u32)) as u32) & 0x1fu32)) as u32)) as u32) & 0xffffu32)) as u32) as u32))) as u32) & 0xffffu32) } else { (if (((((((a as u32)) as u32) << 16) as i32) >> 16)) < 0 { 0xffffu32 } else { 0 as u32 }) })) as u16)
}
