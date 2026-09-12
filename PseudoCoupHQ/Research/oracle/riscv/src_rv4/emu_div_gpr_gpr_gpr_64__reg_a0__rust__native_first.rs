#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of div_gpr_gpr_gpr_64__reg_a0__rust__native_first.
//   If(v0 == 0, 18446744073709551615, If(And(v0 == 18446744073709551615, v1 == 9223372036854775808), 9223372036854775808, bvsdiv_i(v1, v0)))
#[no_mangle]
pub extern "C" fn emu_div_gpr_gpr_gpr_64__reg_a0__rust__native_first(a: u64, b: u64) -> u64
{
    let v0: u64 = ((({ let n1: i64 = (((((b as u64)) as i64)) as i64); let d1: i64 = (((((a as u64)) as i64)) as i64); unsafe { if d1 == 0 || (n1 == i64::MIN && d1 == -1) { core::hint::unreachable_unchecked(); } } n1 / d1 })) as u64);
    let v1: bool = ((((b as u64)) as u64) == ((0x8000000000000000u64) as u64));
    let v2: bool = ((((a as u64)) as u64) == ((0xffffffffffffffffu64) as u64));
    let v3: bool = ((v2) && (v1));
    let v4: u64 = (if (v3) { ((0x8000000000000000u64) as u64) } else { ((v0) as u64) });
    let v5: bool = ((((a as u64)) as u64) == ((0x0u64) as u64));
    let v6: u64 = (if (v5) { ((0xffffffffffffffffu64) as u64) } else { ((v4) as u64) });
    ((v6) as u64)
}
