#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E01546__go_regen_308.
// The term's layer-5 text, LITERAL:
//   Extract(31, 0, v1) >> Concat(0, Extract(4, 0, v0) | ~(31*If(Or(Not(Extract(15, 6, v0) == 0), ULE(32, Extract(5, 0, v0))), 0, 1)))
#[no_mangle]
pub extern "C" fn emu_E01546__go_regen_308(a: u32, b: u16, c: u64) -> u32
{
    (((if ((((((((0x0u32) as u32) << 5) | ((((((((((!(((((((((if (((((((0x20u32) as u32)) <= ((((((((b as u32)) >> 0) as u32) & 0x3fu32)) as u32)))) || ((!(((((((((b as u32)) >> 6) as u32) & 0x3ffu32)) as u32) == ((0x0u32) as u32))))))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u32)).wrapping_mul(((0x1fu32) as u32))) as u32) & 0x1fu32)) as u32)) as u32) & 0x1fu32)) as u32) | (((((((b as u32)) >> 0) as u32) & 0x1fu32)) as u32)) as u32) & 0x1fu32)) as u32)) as u32)) as u32) < (0x20u32)) { ((((((a as u32)) as i32)).wrapping_shr(((((((((0x0u32) as u32) << 5) | ((((((((((!(((((((((if (((((((0x20u32) as u32)) <= ((((((((b as u32)) >> 0) as u32) & 0x3fu32)) as u32)))) || ((!(((((((((b as u32)) >> 6) as u32) & 0x3ffu32)) as u32) == ((0x0u32) as u32))))))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u32)).wrapping_mul(((0x1fu32) as u32))) as u32) & 0x1fu32)) as u32)) as u32) & 0x1fu32)) as u32) | (((((((b as u32)) >> 0) as u32) & 0x1fu32)) as u32)) as u32) & 0x1fu32)) as u32)) as u32)) as u32) as u32))) as u32) } else { (if ((((a as u32)) as i32)) < 0 { 0xffffffffu32 } else { 0 as u32 }) })) as u32)
}
