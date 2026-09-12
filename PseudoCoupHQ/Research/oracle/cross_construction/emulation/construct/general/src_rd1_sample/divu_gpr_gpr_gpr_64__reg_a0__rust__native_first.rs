#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of divu_gpr_gpr_gpr_64__reg_a0__rust__native_first.
//   If(v0 == 0, 18446744073709551615, bvudiv_i(v1, v0))
#[no_mangle]
pub extern "C" fn emu_divu_gpr_gpr_gpr_64__reg_a0__rust__native_first(a: u64, b: u64) -> u64
{
    let v0: u64 = ((({ let n1: u64 = (((b as u64)) as u64); let d1: u64 = (((a as u64)) as u64); unsafe { if d1 == 0 { core::hint::unreachable_unchecked(); } } n1 / d1 })) as u64);
    let v1: bool = ((((a as u64)) as u64) == ((0x0u64) as u64));
    let v2: u64 = (if (v1) { ((0xffffffffffffffffu64) as u64) } else { ((v0) as u64) });
    ((v2) as u64)
}
