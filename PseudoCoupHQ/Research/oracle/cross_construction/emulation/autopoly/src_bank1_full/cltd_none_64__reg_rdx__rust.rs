#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of cltd_none_64__reg_rdx__rust.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(31, 0, v0) >> 31)
#[no_mangle]
pub extern "C" fn emu_cltd_none_64__reg_rdx__rust(a: u32) -> u64
{
    (((((((0x0u32) as u64) << 32) | ((((((((a as u32)) as i32)).wrapping_shr((((0x1fu32) as u32) as u32))) as u32)) as u64)) as u64)) as u64)
}
