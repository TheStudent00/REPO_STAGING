#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of sub_gpr_gpr_16__flags__rust__bit_blast.
//   Concat(Extract(15, 0, v0), Extract(15, 0, v1))
#[no_mangle]
pub extern "C" fn emu_sub_gpr_gpr_16__flags__rust__bit_blast(a: u16, b: u16) -> u32
{
    let x1_0: u32 = (((b) as u32) >> 0) & 1;
    let x1_1: u32 = (((b) as u32) >> 1) & 1;
    let x1_2: u32 = (((b) as u32) >> 2) & 1;
    let x1_3: u32 = (((b) as u32) >> 3) & 1;
    let x1_4: u32 = (((b) as u32) >> 4) & 1;
    let x1_5: u32 = (((b) as u32) >> 5) & 1;
    let x1_6: u32 = (((b) as u32) >> 6) & 1;
    let x1_7: u32 = (((b) as u32) >> 7) & 1;
    let x1_8: u32 = (((b) as u32) >> 8) & 1;
    let x1_9: u32 = (((b) as u32) >> 9) & 1;
    let x1_10: u32 = (((b) as u32) >> 10) & 1;
    let x1_11: u32 = (((b) as u32) >> 11) & 1;
    let x1_12: u32 = (((b) as u32) >> 12) & 1;
    let x1_13: u32 = (((b) as u32) >> 13) & 1;
    let x1_14: u32 = (((b) as u32) >> 14) & 1;
    let x1_15: u32 = (((b) as u32) >> 15) & 1;
    let x0_0: u32 = (((a) as u32) >> 0) & 1;
    let x0_1: u32 = (((a) as u32) >> 1) & 1;
    let x0_2: u32 = (((a) as u32) >> 2) & 1;
    let x0_3: u32 = (((a) as u32) >> 3) & 1;
    let x0_4: u32 = (((a) as u32) >> 4) & 1;
    let x0_5: u32 = (((a) as u32) >> 5) & 1;
    let x0_6: u32 = (((a) as u32) >> 6) & 1;
    let x0_7: u32 = (((a) as u32) >> 7) & 1;
    let x0_8: u32 = (((a) as u32) >> 8) & 1;
    let x0_9: u32 = (((a) as u32) >> 9) & 1;
    let x0_10: u32 = (((a) as u32) >> 10) & 1;
    let x0_11: u32 = (((a) as u32) >> 11) & 1;
    let x0_12: u32 = (((a) as u32) >> 12) & 1;
    let x0_13: u32 = (((a) as u32) >> 13) & 1;
    let x0_14: u32 = (((a) as u32) >> 14) & 1;
    let x0_15: u32 = (((a) as u32) >> 15) & 1;
    let w0: u32 = (x1_0 << 0);
    let w1: u32 = w0 | (x1_1 << 1);
    let w2: u32 = w1 | (x1_2 << 2);
    let w3: u32 = w2 | (x1_3 << 3);
    let w4: u32 = w3 | (x1_4 << 4);
    let w5: u32 = w4 | (x1_5 << 5);
    let w6: u32 = w5 | (x1_6 << 6);
    let w7: u32 = w6 | (x1_7 << 7);
    let w8: u32 = w7 | (x1_8 << 8);
    let w9: u32 = w8 | (x1_9 << 9);
    let w10: u32 = w9 | (x1_10 << 10);
    let w11: u32 = w10 | (x1_11 << 11);
    let w12: u32 = w11 | (x1_12 << 12);
    let w13: u32 = w12 | (x1_13 << 13);
    let w14: u32 = w13 | (x1_14 << 14);
    let w15: u32 = w14 | (x1_15 << 15);
    let w16: u32 = w15 | (x0_0 << 16);
    let w17: u32 = w16 | (x0_1 << 17);
    let w18: u32 = w17 | (x0_2 << 18);
    let w19: u32 = w18 | (x0_3 << 19);
    let w20: u32 = w19 | (x0_4 << 20);
    let w21: u32 = w20 | (x0_5 << 21);
    let w22: u32 = w21 | (x0_6 << 22);
    let w23: u32 = w22 | (x0_7 << 23);
    let w24: u32 = w23 | (x0_8 << 24);
    let w25: u32 = w24 | (x0_9 << 25);
    let w26: u32 = w25 | (x0_10 << 26);
    let w27: u32 = w26 | (x0_11 << 27);
    let w28: u32 = w27 | (x0_12 << 28);
    let w29: u32 = w28 | (x0_13 << 29);
    let w30: u32 = w29 | (x0_14 << 30);
    let w31: u32 = w30 | (x0_15 << 31);
    ((w31) as u32)
}
