#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of imul_gpr_one_8__reg_rax__rust.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 16, v0), Concat(Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 0, v0))*Concat(Extract(7, 7, v1), Extract(7, 7, v1), Extract(7, 7, v1), Extract(7, 7, v1), Extract(7, 7, v1), Extract(7, 7, v1), Extract(7, 7, v1), Extract(7, 7, v1), Extract(7, 0, v1)))
#[no_mangle]
pub extern "C" fn emu_imul_gpr_one_8__reg_rax__rust(a: u64, b: u8) -> u64
{
    ((((((((((((a as u64)) >> 16) as u64) & 0xffffffffffffu64)) as u64) << 16) | (((((((((((((((((((a as u64)) >> 7) as u32) & 0x1u32)) as u32) << 15) | ((((((((a as u64)) >> 7) as u32) & 0x1u32)) as u32) << 14) | ((((((((a as u64)) >> 7) as u32) & 0x1u32)) as u32) << 13) | ((((((((a as u64)) >> 7) as u32) & 0x1u32)) as u32) << 12) | ((((((((a as u64)) >> 7) as u32) & 0x1u32)) as u32) << 11) | ((((((((a as u64)) >> 7) as u32) & 0x1u32)) as u32) << 10) | ((((((((a as u64)) >> 7) as u32) & 0x1u32)) as u32) << 9) | ((((((((a as u64)) >> 7) as u32) & 0x1u32)) as u32) << 8) | (((((((a as u64)) >> 0) as u32) & 0xffu32)) as u32)) as u32) & 0xffffu32)) as u32)).wrapping_mul((((((((((((((b as u32)) >> 7) as u32) & 0x1u32)) as u32) << 15) | ((((((((b as u32)) >> 7) as u32) & 0x1u32)) as u32) << 14) | ((((((((b as u32)) >> 7) as u32) & 0x1u32)) as u32) << 13) | ((((((((b as u32)) >> 7) as u32) & 0x1u32)) as u32) << 12) | ((((((((b as u32)) >> 7) as u32) & 0x1u32)) as u32) << 11) | ((((((((b as u32)) >> 7) as u32) & 0x1u32)) as u32) << 10) | ((((((((b as u32)) >> 7) as u32) & 0x1u32)) as u32) << 9) | ((((((((b as u32)) >> 7) as u32) & 0x1u32)) as u32) << 8) | (((b as u32)) as u32)) as u32) & 0xffffu32)) as u32))) as u32) & 0xffffu32)) as u64)) as u64)) as u64)
}
