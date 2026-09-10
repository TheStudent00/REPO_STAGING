#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of setle_gpr_one_8__reg_rdi__rust.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(~(~Extract(7, 0, v0) | ~Extract(7, 0, v1)) <= 0, 1, 0))
#[no_mangle]
pub extern "C" fn emu_setle_gpr_one_8__reg_rdi__rust(a: u8, b: u8) -> u64
{
    (((((((0x0u64) as u64) << 8) | (((if (((((((((((!((((((((((!(((b as u32)) as u32)) as u32) & 0xffu32)) as u32) | (((((!(((a as u32)) as u32)) as u32) & 0xffu32)) as u32)) as u32) & 0xffu32)) as u32)) as u32) & 0xffu32)) as u32) << 24) as i32) >> 24)) <= ((((((0x0u32) as u32) << 24) as i32) >> 24)))) { ((0x1u32) as u32) } else { ((0x0u32) as u32) })) as u64)) as u64)) as u64)
}
