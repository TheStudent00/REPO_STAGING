#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of remw_gpr_gpr_same_32__reg_a0__rust__native_first.
//   Concat(If(Extract(31, 0, v0) == 0, Extract(31, 31, v0), If(And(Extract(31, 0, v0) == 2147483648, Extract(31, 0, v0) == 4294967295), 0, Extract(31, 31, bvsrem_i(Extract(31, 0, v0), Extract(31, 0, v0))))), If(Extract(31, 0, v0) == 0, Extract(31, 31, v0), If(And(Extract(31, 0, v0) == 2147483648, Extract(31, 0, v0) == 4294967295), 0, Extract(31, 31, bvsrem_i(Extract(31, 0, v0), Extract(31, 0, v0))))), If(Extract(31, 0, v0) == 0, Extract(31, 31, v0), If(And(Extract(31, 0, v0) == 2147483648, Extract(31, 0, v0) == 4294967295), 0, Extract(31, 31, bvsrem_i(Extract(31, 0, v0), Extract(31, 0, v0))))), If(Extract(31, 0, v0) == 0, Extract(31, 31, v0), If(And(Extract(31, 0, v0) == 2147483648, Extract(31, 0, v0) == 4294967295), 0, Extract(31, 31, bvsrem_i(Extract(31, 0, v0), Extract(31, 0, v0))))), If(Extract(31, 0, v0) == 0, Extract(31, 31, v0), If(And(Extract(31, 0, v0) == 2147483648, Extract(31, 0, 
#[no_mangle]
pub extern "C" fn emu_remw_gpr_gpr_same_32__reg_a0__rust__native_first(a: u32) -> u64
{
    let v0: u32 = (a as u32);
    let v1: u32 = ((({ let n1: i32 = ((((v0) as i32)) as i32); let d1: i32 = ((((v0) as i32)) as i32); unsafe { if d1 == 0 || (n1 == i32::MIN && d1 == -1) { core::hint::unreachable_unchecked(); } } n1 % d1 })) as u32);
    let v2: bool = (((v0) as u32) == ((0xffffffffu32) as u32));
    let v3: bool = (((v0) as u32) == ((0x80000000u32) as u32));
    let v4: bool = ((v3) && (v2));
    let v5: u32 = (if (v4) { ((0x0u32) as u32) } else { ((v1) as u32) });
    let v6: bool = (((v0) as u32) == ((0x0u32) as u32));
    let v7: u32 = (if (v6) { ((v0) as u32) } else { ((v5) as u32) });
    let v8: u32 = (((((v1) as u32) >> 31) as u32) & 0x1u32);
    let v9: u32 = (if (v4) { ((0x0u32) as u32) } else { ((v8) as u32) });
    let v10: u32 = (((((a as u32)) >> 31) as u32) & 0x1u32);
    let v11: u32 = (if (v6) { ((v10) as u32) } else { ((v9) as u32) });
    let v12: u64 = (((((v11) as u64) << 63) | (((v11) as u64) << 62) | (((v11) as u64) << 61) | (((v11) as u64) << 60) | (((v11) as u64) << 59) | (((v11) as u64) << 58) | (((v11) as u64) << 57) | (((v11) as u64) << 56) | (((v11) as u64) << 55) | (((v11) as u64) << 54) | (((v11) as u64) << 53) | (((v11) as u64) << 52) | (((v11) as u64) << 51) | (((v11) as u64) << 50) | (((v11) as u64) << 49) | (((v11) as u64) << 48) | (((v11) as u64) << 47) | (((v11) as u64) << 46) | (((v11) as u64) << 45) | (((v11) as u64) << 44) | (((v11) as u64) << 43) | (((v11) as u64) << 42) | (((v11) as u64) << 41) | (((v11) as u64) << 40) | (((v11) as u64) << 39) | (((v11) as u64) << 38) | (((v11) as u64) << 37) | (((v11) as u64) << 36) | (((v11) as u64) << 35) | (((v11) as u64) << 34) | (((v11) as u64) << 33) | (((v11) as u64) << 32) | ((v7) as u64)) as u64);
    ((v12) as u64)
}
