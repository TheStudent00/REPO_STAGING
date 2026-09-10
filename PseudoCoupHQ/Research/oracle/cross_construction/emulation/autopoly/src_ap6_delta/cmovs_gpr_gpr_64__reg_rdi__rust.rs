#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of cmovs_gpr_gpr_64__reg_rdi__rust.
// The term's layer-5 text, LITERAL:
//   If(0 <= ~(~Extract(63, 0, v0) | ~v1), v2, v3)
#[no_mangle]
pub extern "C" fn emu_cmovs_gpr_gpr_64__reg_rdi__rust(a: u64, b: u64, c: u64, d: u64) -> u64
{
    (((if (((((0x0u64) as i64)) <= (((((!((((((((!(((b as u64)) as u64)) as u64)) as u64) | ((((!(((a as u64)) as u64)) as u64)) as u64)) as u64)) as u64)) as u64)) as i64)))) { (((d as u64)) as u64) } else { (((c as u64)) as u64) })) as u64)
}
