#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of test_imm_gpr_64__flags_high__rust.
// The term's layer-5 text, LITERAL:
//   ~(~v0 | ~v1)
#[no_mangle]
pub extern "C" fn emu_test_imm_gpr_64__flags_high__rust(a: u64, b: u64) -> u64
{
    ((((!((((((((!(((a as u64)) as u64)) as u64)) as u64) | ((((!(((b as u64)) as u64)) as u64)) as u64)) as u64)) as u64)) as u64)) as u64)
}
