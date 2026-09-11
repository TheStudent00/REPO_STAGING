#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of setae_gpr_one_8__reg_rdi__rust__native_first.
//   Concat(Extract(63, 8, v0), If(ULE(Extract(7, 0, v1), Extract(7, 0, v2)), 1, 0))
#[no_mangle]
pub extern "C" fn emu_setae_gpr_one_8__reg_rdi__rust__native_first(a: u8, b: u8, c: u64) -> u64
{
    let v0: u32 = (a as u32);
    let v1: u32 = (b as u32);
    let v2: bool = ((((v1) as u32)) <= (((v0) as u32)));
    let v3: u32 = (if (v2) { ((0x1u32) as u32) } else { ((0x0u32) as u32) });
    let v4: u64 = (((((c as u64)) >> 8) as u64) & 0xffffffffffffffu64);
    let v5: u64 = (((((v4) as u64) << 8) | ((v3) as u64)) as u64);
    ((v5) as u64)
}
