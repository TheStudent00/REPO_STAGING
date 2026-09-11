#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of div_gpr_one_64__reg_rax__rust__native_first.
//   Extract(63, 0, bvudiv_i(Concat(v0, v1), Concat(0, v2)))
#[no_mangle]
pub extern "C" fn emu_div_gpr_one_64__reg_rax__rust__native_first(a: u64, b: u64, c: u64) -> u64
{
    let v0: u128 = (((((0x0u64) as u128) << 64) | (((c as u64)) as u128)) as u128);
    let v1: u128 = ((((((a as u64)) as u128) << 64) | (((b as u64)) as u128)) as u128);
    let v2: u128 = ((({ let n1: u128 = ((v1) as u128); let d1: u128 = ((v0) as u128); unsafe { if d1 == 0 { core::hint::unreachable_unchecked(); } } n1 / d1 })) as u128);
    let v3: u64 = ((((v2) as u128) >> 0) as u64);
    ((v3) as u64)
}
