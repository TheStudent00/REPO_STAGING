#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of div_gpr_one_32__reg_rdx__rust.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(31, 0, bvurem_i(Concat(Extract(31, 0, v0), Extract(31, 0, v1)), Concat(0, Extract(31, 0, v2)))))
#[no_mangle]
pub extern "C" fn emu_div_gpr_one_32__reg_rdx__rust(a: u32, b: u32, c: u32) -> u64
{
    (((((((0x0u32) as u64) << 32) | ((((((((({ let n1: u64 = ((((((((a as u32)) as u64) << 32) | (((b as u32)) as u64)) as u64)) as u64); let d1: u64 = (((((((0x0u32) as u64) << 32) | (((c as u32)) as u64)) as u64)) as u64); unsafe { if d1 == 0 { core::hint::unreachable_unchecked(); } } n1 % d1 })) as u64)) as u64) >> 0) as u32)) as u64)) as u64)) as u64)
}
