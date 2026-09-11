#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of setg_gpr_one_8__reg_rdi__rust__native_first.
//   Concat(Extract(63, 8, v2), If(And(Extract(7, 7, Extract(7, 0, v0)*255 + Extract(7, 0, v1)) == If(Extract(7, 7, Concat(Extract(7, 7, v0), Extract(7, 0, v0))*511 + Concat(Extract(7, 7, v1), Extract(7, 0, v1))) == Extract(8, 8, Concat(Extract(7, 7, v0), Extract(7, 0, v0))*511 + Concat(Extract(7, 7, v1), Extract(7, 0, v1))), 0, 1), Not(Extract(7, 0, v0) == Extract(7, 0, v1))), 1, 0))
#[no_mangle]
pub extern "C" fn emu_setg_gpr_one_8__reg_rdi__rust__native_first(a: u8, b: u8, c: u64) -> u64
{
    let v0: u32 = (a as u32);
    let v1: u32 = (b as u32);
    let v2: bool = (((v1) as u32) == ((v0) as u32));
    let v3: bool = (!(v2));
    let v4: u32 = (((((a as u32)) >> 7) as u32) & 0x1u32);
    let v5: u32 = ((((((v4) as u32) << 8) | ((v0) as u32)) as u32) & 0x1ffu32);
    let v6: u32 = (((((b as u32)) >> 7) as u32) & 0x1u32);
    let v7: u32 = ((((((v6) as u32) << 8) | ((v1) as u32)) as u32) & 0x1ffu32);
    let v8: u32 = ((((((v7) as u32)).wrapping_mul(((0x1ffu32) as u32))) as u32) & 0x1ffu32);
    let v9: u32 = ((((((v8) as u32)).wrapping_add(((v5) as u32))) as u32) & 0x1ffu32);
    let v10: u32 = (((((v9) as u32) >> 8) as u32) & 0x1u32);
    let v11: u32 = (((((v9) as u32) >> 7) as u32) & 0x1u32);
    let v12: bool = (((v11) as u32) == ((v10) as u32));
    let v13: u32 = (if (v12) { ((0x0u32) as u32) } else { ((0x1u32) as u32) });
    let v14: u32 = ((((((v1) as u32)).wrapping_mul(((0xffu32) as u32))) as u32) & 0xffu32);
    let v15: u32 = ((((((v14) as u32)).wrapping_add(((v0) as u32))) as u32) & 0xffu32);
    let v16: u32 = (((((v15) as u32) >> 7) as u32) & 0x1u32);
    let v17: bool = (((v16) as u32) == ((v13) as u32));
    let v18: bool = ((v17) && (v3));
    let v19: u32 = (if (v18) { ((0x1u32) as u32) } else { ((0x0u32) as u32) });
    let v20: u64 = (((((c as u64)) >> 8) as u64) & 0xffffffffffffffu64);
    let v21: u64 = (((((v20) as u64) << 8) | ((v19) as u64)) as u64);
    ((v21) as u64)
}
