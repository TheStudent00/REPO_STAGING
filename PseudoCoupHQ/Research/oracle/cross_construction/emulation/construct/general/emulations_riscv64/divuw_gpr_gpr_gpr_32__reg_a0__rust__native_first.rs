#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of divuw_gpr_gpr_gpr_32__reg_a0__rust__native_first.
//   Concat(If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If
#[no_mangle]
pub extern "C" fn emu_divuw_gpr_gpr_gpr_32__reg_a0__rust__native_first(a: u32, b: u32) -> u64
{
    let v0: u32 = (a as u32);
    let v1: u32 = (b as u32);
    let v2: u32 = ((({ let n1: u32 = ((v1) as u32); let d1: u32 = ((v0) as u32); unsafe { if d1 == 0 { core::hint::unreachable_unchecked(); } } n1 / d1 })) as u32);
    let v3: bool = (((v0) as u32) == ((0x0u32) as u32));
    let v4: u32 = (if (v3) { ((0xffffffffu32) as u32) } else { ((v2) as u32) });
    let v5: u32 = (((((v2) as u32) >> 31) as u32) & 0x1u32);
    let v6: u32 = (if (v3) { ((0x1u32) as u32) } else { ((v5) as u32) });
    let v7: u64 = (((((v6) as u64) << 63) | (((v6) as u64) << 62) | (((v6) as u64) << 61) | (((v6) as u64) << 60) | (((v6) as u64) << 59) | (((v6) as u64) << 58) | (((v6) as u64) << 57) | (((v6) as u64) << 56) | (((v6) as u64) << 55) | (((v6) as u64) << 54) | (((v6) as u64) << 53) | (((v6) as u64) << 52) | (((v6) as u64) << 51) | (((v6) as u64) << 50) | (((v6) as u64) << 49) | (((v6) as u64) << 48) | (((v6) as u64) << 47) | (((v6) as u64) << 46) | (((v6) as u64) << 45) | (((v6) as u64) << 44) | (((v6) as u64) << 43) | (((v6) as u64) << 42) | (((v6) as u64) << 41) | (((v6) as u64) << 40) | (((v6) as u64) << 39) | (((v6) as u64) << 38) | (((v6) as u64) << 37) | (((v6) as u64) << 36) | (((v6) as u64) << 35) | (((v6) as u64) << 34) | (((v6) as u64) << 33) | (((v6) as u64) << 32) | ((v4) as u64)) as u64);
    ((v7) as u64)
}
