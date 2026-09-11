#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of setg_gpr_one_8__reg_rdi__rust.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 8, v2), If(And(Extract(7, 7, Extract(7, 0, v0)*255 + Extract(7, 0, v1)) == If(Extract(7, 7, Concat(Extract(7, 7, v0), Extract(7, 0, v0))*511 + Concat(Extract(7, 7, v1), Extract(7, 0, v1))) == Extract(8, 8, Concat(Extract(7, 7, v0), Extract(7, 0, v0))*511 + Concat(Extract(7, 7, v1), Extract(7, 0, v1))), 0, 1), Not(Extract(7, 0, v0) == Extract(7, 0, v1))), 1, 0))
#[no_mangle]
pub extern "C" fn emu_setg_gpr_one_8__reg_rdi__rust(a: u8, b: u8, c: u64) -> u64
{
    ((((((((((((c as u64)) >> 8) as u64) & 0xffffffffffffffu64)) as u64) << 8) | (((if ((((((((((((((((((((((((b as u32)) as u32)).wrapping_mul(((0xffu32) as u32))) as u32) & 0xffu32)) as u32)).wrapping_add((((a as u32)) as u32))) as u32) & 0xffu32)) as u32) >> 7) as u32) & 0x1u32)) as u32) == (((if ((((((((((((((((((((((((((((((((b as u32)) >> 7) as u32) & 0x1u32)) as u32) << 8) | (((b as u32)) as u32)) as u32) & 0x1ffu32)) as u32)).wrapping_mul(((0x1ffu32) as u32))) as u32) & 0x1ffu32)) as u32)).wrapping_add((((((((((((((a as u32)) >> 7) as u32) & 0x1u32)) as u32) << 8) | (((a as u32)) as u32)) as u32) & 0x1ffu32)) as u32))) as u32) & 0x1ffu32)) as u32) >> 7) as u32) & 0x1u32)) as u32) == ((((((((((((((((((((((((((((((b as u32)) >> 7) as u32) & 0x1u32)) as u32) << 8) | (((b as u32)) as u32)) as u32) & 0x1ffu32)) as u32)).wrapping_mul(((0x1ffu32) as u32))) as u32) & 0x1ffu32)) as u32)).wrapping_add((((((((((((((a as u32)) >> 7) as u32) & 0x1u32)) as u32) << 8) | (((a as u32)) as u32)) as u32) & 0x1ffu32)) as u32))) as u32) & 0x1ffu32)) as u32) >> 8) as u32) & 0x1u32)) as u32))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u32))) && ((!(((((b as u32)) as u32) == (((a as u32)) as u32))))))) { ((0x1u32) as u32) } else { ((0x0u32) as u32) })) as u64)) as u64)) as u64)
}
