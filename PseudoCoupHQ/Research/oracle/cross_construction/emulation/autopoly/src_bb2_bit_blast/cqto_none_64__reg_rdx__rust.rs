#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of cqto_none_64__reg_rdx__rust.
// The term's layer-5 text, LITERAL:
//   v0 >> 63
#[no_mangle]
pub extern "C" fn emu_cqto_none_64__reg_rdx__rust(a: u64) -> u64
{
    ((((((((a as u64)) as i64)).wrapping_shr((((0x3fu64) as u64) as u32))) as u64)) as u64)
}
