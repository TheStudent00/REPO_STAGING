#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of movswl_widen_gpr_gpr_32__reg_rdi__rust.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 0, v0))
#[no_mangle]
pub extern "C" fn emu_movswl_widen_gpr_gpr_32__reg_rdi__rust(a: u16) -> u64
{
    (((((((0x0u32) as u64) << 32) | ((((((((a as u32)) >> 15) as u32) & 0x1u32)) as u64) << 31) | ((((((((a as u32)) >> 15) as u32) & 0x1u32)) as u64) << 30) | ((((((((a as u32)) >> 15) as u32) & 0x1u32)) as u64) << 29) | ((((((((a as u32)) >> 15) as u32) & 0x1u32)) as u64) << 28) | ((((((((a as u32)) >> 15) as u32) & 0x1u32)) as u64) << 27) | ((((((((a as u32)) >> 15) as u32) & 0x1u32)) as u64) << 26) | ((((((((a as u32)) >> 15) as u32) & 0x1u32)) as u64) << 25) | ((((((((a as u32)) >> 15) as u32) & 0x1u32)) as u64) << 24) | ((((((((a as u32)) >> 15) as u32) & 0x1u32)) as u64) << 23) | ((((((((a as u32)) >> 15) as u32) & 0x1u32)) as u64) << 22) | ((((((((a as u32)) >> 15) as u32) & 0x1u32)) as u64) << 21) | ((((((((a as u32)) >> 15) as u32) & 0x1u32)) as u64) << 20) | ((((((((a as u32)) >> 15) as u32) & 0x1u32)) as u64) << 19) | ((((((((a as u32)) >> 15) as u32) & 0x1u32)) as u64) << 18) | ((((((((a as u32)) >> 15) as u32) & 0x1u32)) as u64) << 17) | ((((((((a as u32)) >> 15) as u32) & 0x1u32)) as u64) << 16) | (((a as u32)) as u64)) as u64)) as u64)
}
