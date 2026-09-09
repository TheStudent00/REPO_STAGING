#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of shrd_cl_gpr_gpr_64__reg_rdi__rust.
// The term's layer-5 text, LITERAL:
//   Extract(63, 0, LShR(Concat(v0, v1), Concat(0, Extract(5, 0, v2))))
#[no_mangle]
pub extern "C" fn emu_shrd_cl_gpr_gpr_64__reg_rdi__rust(a: u64, b: u64, c: u8) -> u64
{
    ((((((((((((((((a as u64)) as u128) << 64) | (((b as u64)) as u128)) as u128)) as u128).wrapping_shr(((((((((0x0u128) as u128) << 6) | (((((((c as u32)) >> 0) as u32) & 0x3fu32)) as u128)) as u128)) as u128) as u32))) as u128)) as u128) >> 0) as u64)) as u64)
}
