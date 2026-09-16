#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of REMW__is_unsigned_True__rd__rust__native_first.
//   
#[no_mangle]
pub extern "C" fn emu_REMW__is_unsigned_True__rd__rust__native_first(a: u32, b: u32) -> u64
{
    let v0: u32 = (a as u32);
    let v1: u128 = (((((0x0u128) as u128) << 32) | ((v0) as u128)) as u128);
    let v2: u32 = (b as u32);
    let v3: u128 = (((((0x0u128) as u128) << 32) | ((v2) as u128)) as u128);
    let v4: u128 = ((({ let n1: i128 = ((((v3) as i128)) as i128); let d1: i128 = ((((v1) as i128)) as i128); unsafe { if d1 == 0 || (n1 == i128::MIN && d1 == -1) { core::hint::unreachable_unchecked(); } } n1 % d1 })) as u128);
    let v5: u32 = ((((v4) as u128) >> 0) as u32);
    let v6: bool = (((v0) as u32) == ((0x0u32) as u32));
    let v7: u32 = (if (v6) { ((v2) as u32) } else { ((v5) as u32) });
    let v8: u32 = (((((v4) as u128) >> 31) as u32) & 0x1u32);
    let v9: u32 = (((((b as u32)) >> 31) as u32) & 0x1u32);
    let v10: u32 = (if (v6) { ((v9) as u32) } else { ((v8) as u32) });
    let v11: u64 = (((((v10) as u64) << 63) | (((v10) as u64) << 62) | (((v10) as u64) << 61) | (((v10) as u64) << 60) | (((v10) as u64) << 59) | (((v10) as u64) << 58) | (((v10) as u64) << 57) | (((v10) as u64) << 56) | (((v10) as u64) << 55) | (((v10) as u64) << 54) | (((v10) as u64) << 53) | (((v10) as u64) << 52) | (((v10) as u64) << 51) | (((v10) as u64) << 50) | (((v10) as u64) << 49) | (((v10) as u64) << 48) | (((v10) as u64) << 47) | (((v10) as u64) << 46) | (((v10) as u64) << 45) | (((v10) as u64) << 44) | (((v10) as u64) << 43) | (((v10) as u64) << 42) | (((v10) as u64) << 41) | (((v10) as u64) << 40) | (((v10) as u64) << 39) | (((v10) as u64) << 38) | (((v10) as u64) << 37) | (((v10) as u64) << 36) | (((v10) as u64) << 35) | (((v10) as u64) << 34) | (((v10) as u64) << 33) | (((v10) as u64) << 32) | ((v7) as u64)) as u64);
    ((v11) as u64)
}
