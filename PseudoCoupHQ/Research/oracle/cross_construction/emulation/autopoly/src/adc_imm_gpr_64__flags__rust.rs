#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of adc_imm_gpr_64__flags__rust.
// The term's layer-5 text, LITERAL:
//   Concat(v0, 3)
#[no_mangle]
pub extern "C" fn emu_adc_imm_gpr_64__flags__rust(a: u64) -> u128
{
    ((((((((a as u64)) as u128) << 64) | ((0x3u64) as u128)) as u128)) as u128)
}
