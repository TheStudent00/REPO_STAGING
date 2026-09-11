#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of idiv_gpr_one_32__reg_rax__rust__native_first.
//   Concat(0, Extract(31, 0, bvsdiv_i(Concat(Extract(31, 0, v0), Extract(31, 0, v1)), Concat(Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 0, v2)))))
#[no_mangle]
pub extern "C" fn emu_idiv_gpr_one_32__reg_rax__rust__native_first(a: u32, b: u32, c: u32) -> u64
{
    let v0: u32 = (c as u32);
    let v1: u32 = (((((c as u32)) >> 31) as u32) & 0x1u32);
    let v2: u64 = (((((v1) as u64) << 63) | (((v1) as u64) << 62) | (((v1) as u64) << 61) | (((v1) as u64) << 60) | (((v1) as u64) << 59) | (((v1) as u64) << 58) | (((v1) as u64) << 57) | (((v1) as u64) << 56) | (((v1) as u64) << 55) | (((v1) as u64) << 54) | (((v1) as u64) << 53) | (((v1) as u64) << 52) | (((v1) as u64) << 51) | (((v1) as u64) << 50) | (((v1) as u64) << 49) | (((v1) as u64) << 48) | (((v1) as u64) << 47) | (((v1) as u64) << 46) | (((v1) as u64) << 45) | (((v1) as u64) << 44) | (((v1) as u64) << 43) | (((v1) as u64) << 42) | (((v1) as u64) << 41) | (((v1) as u64) << 40) | (((v1) as u64) << 39) | (((v1) as u64) << 38) | (((v1) as u64) << 37) | (((v1) as u64) << 36) | (((v1) as u64) << 35) | (((v1) as u64) << 34) | (((v1) as u64) << 33) | (((v1) as u64) << 32) | ((v0) as u64)) as u64);
    let v3: u32 = (b as u32);
    let v4: u32 = (a as u32);
    let v5: u64 = (((((v4) as u64) << 32) | ((v3) as u64)) as u64);
    let v6: u64 = ((({ let n1: i64 = ((((v5) as i64)) as i64); let d1: i64 = ((((v2) as i64)) as i64); unsafe { if d1 == 0 || (n1 == i64::MIN && d1 == -1) { core::hint::unreachable_unchecked(); } } n1 / d1 })) as u64);
    let v7: u32 = ((((v6) as u64) >> 0) as u32);
    let v8: u64 = (((((0x0u32) as u64) << 32) | ((v7) as u64)) as u64);
    ((v8) as u64)
}
