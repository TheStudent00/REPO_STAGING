#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of seta_gpr_one_8__reg_rdi__rust__native_first.
//   Concat(Extract(63, 8, v2), If(And(ULE(Extract(7, 0, v0), Extract(7, 0, v1)), Not(Extract(7, 0, v0) == Extract(7, 0, v1))), 1, 0))
#[no_mangle]
pub extern "C" fn emu_seta_gpr_one_8__reg_rdi__rust__native_first(a: u8, b: u8, c: u64) -> u64
{
    let v0: u32 = (a as u32);
    let v1: u32 = (b as u32);
    let v2: bool = (((v1) as u32) == ((v0) as u32));
    let v3: bool = (!(v2));
    let v4: bool = ((((v1) as u32)) <= (((v0) as u32)));
    let v5: bool = ((v4) && (v3));
    let v6: u32 = (if (v5) { ((0x1u32) as u32) } else { ((0x0u32) as u32) });
    let v7: u64 = (((((c as u64)) >> 8) as u64) & 0xffffffffffffffu64);
    let v8: u64 = (((((v7) as u64) << 8) | ((v6) as u64)) as u64);
    ((v8) as u64)
}
