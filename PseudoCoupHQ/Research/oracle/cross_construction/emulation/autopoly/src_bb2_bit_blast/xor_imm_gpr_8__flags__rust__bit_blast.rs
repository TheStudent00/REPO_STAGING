#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of xor_imm_gpr_8__flags__rust__bit_blast.
//   Concat(Extract(7, 0, v0) ^ Extract(7, 0, v1), 0)
#[no_mangle]
pub extern "C" fn emu_xor_imm_gpr_8__flags__rust__bit_blast(a: u8, b: u8) -> u16
{
    let x1_0: u32 = (((a) as u32) >> 0) & 1;
    let x0_0: u32 = (((b) as u32) >> 0) & 1;
    let x1_1: u32 = (((a) as u32) >> 1) & 1;
    let x0_1: u32 = (((b) as u32) >> 1) & 1;
    let x1_2: u32 = (((a) as u32) >> 2) & 1;
    let x0_2: u32 = (((b) as u32) >> 2) & 1;
    let x1_3: u32 = (((a) as u32) >> 3) & 1;
    let x0_3: u32 = (((b) as u32) >> 3) & 1;
    let x1_4: u32 = (((a) as u32) >> 4) & 1;
    let x0_4: u32 = (((b) as u32) >> 4) & 1;
    let x1_5: u32 = (((a) as u32) >> 5) & 1;
    let x0_5: u32 = (((b) as u32) >> 5) & 1;
    let x1_6: u32 = (((a) as u32) >> 6) & 1;
    let x0_6: u32 = (((b) as u32) >> 6) & 1;
    let x1_7: u32 = (((a) as u32) >> 7) & 1;
    let x0_7: u32 = (((b) as u32) >> 7) & 1;
    let k0: u32 = 0;
    let g0: u32 = (x0_0 ^ x1_0);
    let g1: u32 = (g0 ^ 1);
    let g2: u32 = (g1 ^ 1);
    let g3: u32 = (x0_1 ^ x1_1);
    let g4: u32 = (g3 ^ 1);
    let g5: u32 = (g4 ^ 1);
    let g6: u32 = (x0_2 ^ x1_2);
    let g7: u32 = (g6 ^ 1);
    let g8: u32 = (g7 ^ 1);
    let g9: u32 = (x0_3 ^ x1_3);
    let g10: u32 = (g9 ^ 1);
    let g11: u32 = (g10 ^ 1);
    let g12: u32 = (x0_4 ^ x1_4);
    let g13: u32 = (g12 ^ 1);
    let g14: u32 = (g13 ^ 1);
    let g15: u32 = (x0_5 ^ x1_5);
    let g16: u32 = (g15 ^ 1);
    let g17: u32 = (g16 ^ 1);
    let g18: u32 = (x0_6 ^ x1_6);
    let g19: u32 = (g18 ^ 1);
    let g20: u32 = (g19 ^ 1);
    let g21: u32 = (x0_7 ^ x1_7);
    let g22: u32 = (g21 ^ 1);
    let g23: u32 = (g22 ^ 1);
    let w0: u32 = (k0 << 0);
    let w1: u32 = w0 | (k0 << 1);
    let w2: u32 = w1 | (k0 << 2);
    let w3: u32 = w2 | (k0 << 3);
    let w4: u32 = w3 | (k0 << 4);
    let w5: u32 = w4 | (k0 << 5);
    let w6: u32 = w5 | (k0 << 6);
    let w7: u32 = w6 | (k0 << 7);
    let w8: u32 = w7 | (g2 << 8);
    let w9: u32 = w8 | (g5 << 9);
    let w10: u32 = w9 | (g8 << 10);
    let w11: u32 = w10 | (g11 << 11);
    let w12: u32 = w11 | (g14 << 12);
    let w13: u32 = w12 | (g17 << 13);
    let w14: u32 = w13 | (g20 << 14);
    let w15: u32 = w14 | (g23 << 15);
    ((w15) as u16)
}
