#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of REM__is_unsigned_True__rd__rust__native_first.
//   
#[no_mangle]
pub extern "C" fn emu_REM__is_unsigned_True__rd__rust__native_first(a: u64, b: u64) -> u64
{
    let v0: u128 = (((((0x0u64) as u128) << 64) | (((a as u64)) as u128)) as u128);
    let v1: u128 = (((((0x0u64) as u128) << 64) | (((b as u64)) as u128)) as u128);
    let v2: u128 = ((({ let n1: i128 = ((((v1) as i128)) as i128); let d1: i128 = ((((v0) as i128)) as i128); unsafe { if d1 == 0 || (n1 == i128::MIN && d1 == -1) { core::hint::unreachable_unchecked(); } } n1 % d1 })) as u128);
    let v3: u64 = ((((v2) as u128) >> 0) as u64);
    let v4: bool = ((((a as u64)) as u64) == ((0x0u64) as u64));
    let v5: u64 = (if (v4) { (((b as u64)) as u64) } else { ((v3) as u64) });
    ((v5) as u64)
}
