#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of mul_gpr_one_64__reg_rdx__rust.
// The term's layer-5 text, LITERAL:
//   Extract(127, 64, Concat(0, v0)*Concat(0, v1))
#[no_mangle]
pub extern "C" fn emu_mul_gpr_one_64__reg_rdx__rust(a: u64, b: u64) -> u64
{
    ((((((((((((((((0x0u64) as u128) << 64) | (((a as u64)) as u128)) as u128)) as u128)).wrapping_mul((((((((0x0u64) as u128) << 64) | (((b as u64)) as u128)) as u128)) as u128))) as u128)) as u128) >> 64) as u64)) as u64)
}
