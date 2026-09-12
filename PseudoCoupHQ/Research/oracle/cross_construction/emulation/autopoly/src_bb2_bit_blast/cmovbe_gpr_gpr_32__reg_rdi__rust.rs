#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of cmovbe_gpr_gpr_32__reg_rdi__rust.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(Or(Extract(31, 0, v1)*4294967295 == Extract(31, 0, v0), Extract(32, 32, Concat(0, Extract(31, 0, v0)) + Concat(0, Extract(31, 0, v1))) == 1), Extract(31, 0, v2), Extract(31, 0, v3)))
#[no_mangle]
pub extern "C" fn emu_cmovbe_gpr_gpr_32__reg_rdi__rust(a: u32, b: u32, c: u32, d: u32) -> u64
{
    (((((((0x0u32) as u64) << 32) | (((if ((((((((((((a as u32)) as u32)).wrapping_mul(((0xffffffffu32) as u32))) as u32)) as u32) == (((b as u32)) as u32))) || (((((((((((((((((((((0x0u32) as u64) << 32) | (((b as u32)) as u64)) as u64) & 0x1ffffffffu64)) as u64)).wrapping_add(((((((((0x0u32) as u64) << 32) | (((a as u32)) as u64)) as u64) & 0x1ffffffffu64)) as u64))) as u64) & 0x1ffffffffu64)) as u64) >> 32) as u32) & 0x1u32)) as u32) == ((0x1u32) as u32))))) { (((c as u32)) as u32) } else { (((d as u32)) as u32) })) as u64)) as u64)) as u64)
}
