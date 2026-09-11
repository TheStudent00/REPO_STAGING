#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of sbb_imm_gpr_8__reg_rdi__rust.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 8, v3), Extract(7, 0, v2)*255 + If(Extract(8, 8, Concat(0, Extract(7, 0, v0)) + Concat(0, Extract(7, 0, v1))) == 1, 1, 0)*255 + Extract(7, 0, v3))
#[no_mangle]
pub extern "C" fn emu_sbb_imm_gpr_8__reg_rdi__rust(a: u8, b: u8, c: u64, d: u8) -> u64
{
    ((((((((((((c as u64)) >> 8) as u64) & 0xffffffffffffffu64)) as u64) << 8) | ((((((((((((((((d as u32)) as u32)).wrapping_mul(((0xffu32) as u32))) as u32) & 0xffu32)) as u32)).wrapping_add((((((((((if (((((((((((((((((((((0x0u32) as u32) << 8) | (((b as u32)) as u32)) as u32) & 0x1ffu32)) as u32)).wrapping_add(((((((((0x0u32) as u32) << 8) | (((a as u32)) as u32)) as u32) & 0x1ffu32)) as u32))) as u32) & 0x1ffu32)) as u32) >> 8) as u32) & 0x1u32)) as u32) == ((0x1u32) as u32))) { ((0x1u32) as u32) } else { ((0x0u32) as u32) })) as u32)).wrapping_mul(((0xffu32) as u32))) as u32) & 0xffu32)) as u32))).wrapping_add((((((((c as u64)) >> 0) as u32) & 0xffu32)) as u32))) as u32) & 0xffu32)) as u64)) as u64)) as u64)
}
