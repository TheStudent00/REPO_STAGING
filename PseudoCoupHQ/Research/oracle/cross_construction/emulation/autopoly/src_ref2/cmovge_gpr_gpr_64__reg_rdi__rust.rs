#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of cmovge_gpr_gpr_64__reg_rdi__rust.
// The term's layer-5 text, LITERAL:
//   If(Extract(63, 63, Extract(63, 0, v0)*18446744073709551615 + v1) == If(Extract(63, 63, Concat(Extract(63, 63, v0), Extract(63, 0, v0))*36893488147419103231 + Concat(Extract(63, 63, v1), v1)) == Extract(64, 64, Concat(Extract(63, 63, v0), Extract(63, 0, v0))*36893488147419103231 + Concat(Extract(63, 63, v1), v1)), 0, 1), v2, v3)
#[no_mangle]
pub extern "C" fn emu_cmovge_gpr_gpr_64__reg_rdi__rust(a: u64, b: u64, c: u64, d: u64) -> u64
{
    (((if ((((((((((((((((((((b as u64)) as u64)).wrapping_mul(((0xffffffffffffffffu64) as u64))) as u64)) as u64)).wrapping_add((((a as u64)) as u64))) as u64)) as u64) >> 63) as u32) & 0x1u32)) as u32) == (((if ((((((((((((((((((((((((((((((((b as u64)) >> 63) as u32) & 0x1u32)) as u128) << 64) | (((b as u64)) as u128)) as u128) & 0x1ffffffffffffffffu128)) as u128)).wrapping_mul(((0x1ffffffffffffffffu128) as u128))) as u128) & 0x1ffffffffffffffffu128)) as u128)).wrapping_add((((((((((((((a as u64)) >> 63) as u32) & 0x1u32)) as u128) << 64) | (((a as u64)) as u128)) as u128) & 0x1ffffffffffffffffu128)) as u128))) as u128) & 0x1ffffffffffffffffu128)) as u128) >> 63) as u32) & 0x1u32)) as u32) == ((((((((((((((((((((((((((((((b as u64)) >> 63) as u32) & 0x1u32)) as u128) << 64) | (((b as u64)) as u128)) as u128) & 0x1ffffffffffffffffu128)) as u128)).wrapping_mul(((0x1ffffffffffffffffu128) as u128))) as u128) & 0x1ffffffffffffffffu128)) as u128)).wrapping_add((((((((((((((a as u64)) >> 63) as u32) & 0x1u32)) as u128) << 64) | (((a as u64)) as u128)) as u128) & 0x1ffffffffffffffffu128)) as u128))) as u128) & 0x1ffffffffffffffffu128)) as u128) >> 64) as u32) & 0x1u32)) as u32))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u32))) { (((c as u64)) as u64) } else { (((d as u64)) as u64) })) as u64)
}
