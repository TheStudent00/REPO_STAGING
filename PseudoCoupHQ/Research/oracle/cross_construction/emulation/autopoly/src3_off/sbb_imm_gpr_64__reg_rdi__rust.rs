#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of sbb_imm_gpr_64__reg_rdi__rust.
// The term's layer-5 text, LITERAL:
//   If(Extract(64, 64, Concat(0, v0) + Concat(0, v1)) == 1, 1, 0)*18446744073709551615 + v2 + 18446744073709551613
#[no_mangle]
pub extern "C" fn emu_sbb_imm_gpr_64__reg_rdi__rust(a: u64, b: u64, c: u64) -> u64
{
    ((((((((((((((if (((((((((((((((((((((0x0u32) as u128) << 64) | (((b as u64)) as u128)) as u128) & 0x1ffffffffffffffffu128)) as u128)).wrapping_add(((((((((0x0u32) as u128) << 64) | (((a as u64)) as u128)) as u128) & 0x1ffffffffffffffffu128)) as u128))) as u128) & 0x1ffffffffffffffffu128)) as u128) >> 64) as u32) & 0x1u32)) as u32) == ((0x1u32) as u32))) { ((0x1u64) as u64) } else { ((0x0u64) as u64) })) as u64)).wrapping_mul(((0xffffffffffffffffu64) as u64))) as u64)) as u64)).wrapping_add((((c as u64)) as u64))).wrapping_add(((0xfffffffffffffffdu64) as u64))) as u64)) as u64)
}
