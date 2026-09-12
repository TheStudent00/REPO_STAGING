#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of sltiu_gpr_gpr_imm_64__reg_a0__rust__native_first.
//   If(Or(Extract(1, 0, v0) == 3, Not(Extract(63, 2, v0) == 0)), 0, 1)
#[no_mangle]
pub extern "C" fn emu_sltiu_gpr_gpr_imm_64__reg_a0__rust__native_first(a: u64) -> u64
{
    let v0: u64 = (((((a as u64)) >> 2) as u64) & 0x3fffffffffffffffu64);
    let v1: bool = (((v0) as u64) == ((0x0u64) as u64));
    let v2: bool = (!(v1));
    let v3: u32 = (((((a as u64)) >> 0) as u32) & 0x3u32);
    let v4: bool = (((v3) as u32) == ((0x3u32) as u32));
    let v5: bool = ((v4) || (v2));
    let v6: u64 = (if (v5) { ((0x0u64) as u64) } else { ((0x1u64) as u64) });
    ((v6) as u64)
}
