#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of mul_gpr_one_16__reg_rdx__rust.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 16, v2), Extract(31, 16, Concat(0, Extract(15, 0, v0))*Concat(0, Extract(15, 0, v1))))
#[no_mangle]
pub extern "C" fn emu_mul_gpr_one_16__reg_rdx__rust(a: u16, b: u16, c: u64) -> u64
{
    ((((((((((((c as u64)) >> 16) as u64) & 0xffffffffffffu64)) as u64) << 16) | (((((((((((((((((0x0u32) as u32) << 16) | (((a as u32)) as u32)) as u32)) as u32)).wrapping_mul((((((((0x0u32) as u32) << 16) | (((b as u32)) as u32)) as u32)) as u32))) as u32)) as u32) >> 16) as u32) & 0xffffu32)) as u64)) as u64)) as u64)
}
