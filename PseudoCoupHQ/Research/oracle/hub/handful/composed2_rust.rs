#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of add_gpr_gpr_32__reg_rdi__rust.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(31, 0, v0) + Extract(31, 0, v1))
#[no_mangle]
pub extern "C" fn emu_add_gpr_gpr_32__reg_rdi__rust(a: u32, b: u32) -> u64
{
    (((((((0x0u32) as u64) << 32) | ((((((((a as u32)) as u32)).wrapping_add((((b as u32)) as u32))) as u32)) as u64)) as u64)) as u64)
}

// probe 570 -- binary -
#[no_mangle]
pub fn emu_sub_gpr_gpr_32__primitive__rust(a: i32, b: i32) -> <i32 as core::ops::Sub<i32>>::Output {
    a - b
}

// probe 606 -- binary *
#[no_mangle]
pub fn emu_imul_gpr_gpr_32__primitive__rust(a: i32, b: i32) -> <i32 as core::ops::Mul<i32>>::Output {
    a * b
}

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of add_gpr_gpr_64__reg_rdi__rust.
// The term's layer-5 text, LITERAL:
//   v0 + v1
#[no_mangle]
pub extern "C" fn emu_add_gpr_gpr_64__reg_rdi__rust(a: u64, b: u64) -> u64
{
    ((((((((a as u64)) as u64)).wrapping_add((((b as u64)) as u64))) as u64)) as u64)
}

// probe 577 -- binary -
#[no_mangle]
pub fn emu_sub_gpr_gpr_64__primitive__rust(a: i64, b: i64) -> <i64 as core::ops::Sub<i64>>::Output {
    a - b
}

// probe 613 -- binary *
#[no_mangle]
pub fn emu_imul_gpr_gpr_64__primitive__rust(a: i64, b: i64) -> <i64 as core::ops::Mul<i64>>::Output {
    a * b
}

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of addsd_xmm_xmm_64__reg_xmm0__rust.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(fpToFP(Extract(63, 0, v0)) + fpToFP(Extract(63, 0, v1)))
#[no_mangle]
pub extern "C" fn emu_addsd_xmm_xmm_64__reg_xmm0__rust(a: f64, b: f64) -> f64
{
    f64::from_bits((((((b) + (a))).to_bits() as u64)) as u64)
}

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of mulsd_xmm_xmm_64__reg_xmm0__rust.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(fpToFP(Extract(63, 0, v0)) * fpToFP(Extract(63, 0, v1)))
#[no_mangle]
pub extern "C" fn emu_mulsd_xmm_xmm_64__reg_xmm0__rust(a: f64, b: f64) -> f64
{
    f64::from_bits((((((a) * (b))).to_bits() as u64)) as u64)
}

#[no_mangle]
pub extern "C" fn f1_i32_add_sub(a: i32, b: i32, c: i32) -> i32
{
    let hub_t0: i32 = ((((emu_add_gpr_gpr_32__reg_rdi__rust(((a) as u32), ((b) as u32))) as u32)) as i32);
    let hub_t1: i32 = ((((emu_sub_gpr_gpr_32__primitive__rust(((hub_t0) as i32), ((c) as i32))) as u32)) as i32);
    return hub_t1;
}

#[no_mangle]
pub extern "C" fn f2_i32_add_mul(a: i32, b: i32, c: i32) -> i32
{
    let hub_t0: i32 = ((((emu_add_gpr_gpr_32__reg_rdi__rust(((a) as u32), ((b) as u32))) as u32)) as i32);
    let hub_t1: i32 = ((((emu_imul_gpr_gpr_32__primitive__rust(((hub_t0) as i32), ((c) as i32))) as u32)) as i32);
    return hub_t1;
}

#[no_mangle]
pub extern "C" fn f3_i64_add_sub(a: i64, b: i64, c: i64) -> i64
{
    let hub_t0: i64 = ((((emu_add_gpr_gpr_64__reg_rdi__rust(((a) as u64), ((b) as u64))) as u64)) as i64);
    let hub_t1: i64 = ((((emu_sub_gpr_gpr_64__primitive__rust(((hub_t0) as i64), ((c) as i64))) as u64)) as i64);
    return hub_t1;
}

#[no_mangle]
pub extern "C" fn f4_i64_mul(a: i64, b: i64) -> i64
{
    let hub_t0: i64 = ((((emu_imul_gpr_gpr_64__primitive__rust(((a) as i64), ((b) as i64))) as u64)) as i64);
    return hub_t0;
}

#[no_mangle]
pub extern "C" fn f7_f64_add_mul(a: f64, b: f64, c: f64) -> f64
{
    let hub_t0: f64 = ((emu_addsd_xmm_xmm_64__reg_xmm0__rust(((b) as f64), ((a) as f64))) as f64);
    let hub_t1: f64 = ((emu_mulsd_xmm_xmm_64__reg_xmm0__rust(((hub_t0) as f64), ((c) as f64))) as f64);
    return hub_t1;
}
