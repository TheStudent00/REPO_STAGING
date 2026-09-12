#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of lb_gpr_fpr_8__reg_a0__rust__bit_blast.
//   Concat(Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), 
#[no_mangle]
pub extern "C" fn emu_lb_gpr_fpr_8__reg_a0__rust__bit_blast(a: u8) -> u64
{
    let x0_0: u64 = (((a) as u64) >> 0) & 1;
    let x0_1: u64 = (((a) as u64) >> 1) & 1;
    let x0_2: u64 = (((a) as u64) >> 2) & 1;
    let x0_3: u64 = (((a) as u64) >> 3) & 1;
    let x0_4: u64 = (((a) as u64) >> 4) & 1;
    let x0_5: u64 = (((a) as u64) >> 5) & 1;
    let x0_6: u64 = (((a) as u64) >> 6) & 1;
    let x0_7: u64 = (((a) as u64) >> 7) & 1;
    let w0: u64 = (x0_0 << 0);
    let w1: u64 = w0 | (x0_1 << 1);
    let w2: u64 = w1 | (x0_2 << 2);
    let w3: u64 = w2 | (x0_3 << 3);
    let w4: u64 = w3 | (x0_4 << 4);
    let w5: u64 = w4 | (x0_5 << 5);
    let w6: u64 = w5 | (x0_6 << 6);
    let w7: u64 = w6 | (x0_7 << 7);
    let w8: u64 = w7 | (x0_7 << 8);
    let w9: u64 = w8 | (x0_7 << 9);
    let w10: u64 = w9 | (x0_7 << 10);
    let w11: u64 = w10 | (x0_7 << 11);
    let w12: u64 = w11 | (x0_7 << 12);
    let w13: u64 = w12 | (x0_7 << 13);
    let w14: u64 = w13 | (x0_7 << 14);
    let w15: u64 = w14 | (x0_7 << 15);
    let w16: u64 = w15 | (x0_7 << 16);
    let w17: u64 = w16 | (x0_7 << 17);
    let w18: u64 = w17 | (x0_7 << 18);
    let w19: u64 = w18 | (x0_7 << 19);
    let w20: u64 = w19 | (x0_7 << 20);
    let w21: u64 = w20 | (x0_7 << 21);
    let w22: u64 = w21 | (x0_7 << 22);
    let w23: u64 = w22 | (x0_7 << 23);
    let w24: u64 = w23 | (x0_7 << 24);
    let w25: u64 = w24 | (x0_7 << 25);
    let w26: u64 = w25 | (x0_7 << 26);
    let w27: u64 = w26 | (x0_7 << 27);
    let w28: u64 = w27 | (x0_7 << 28);
    let w29: u64 = w28 | (x0_7 << 29);
    let w30: u64 = w29 | (x0_7 << 30);
    let w31: u64 = w30 | (x0_7 << 31);
    let w32: u64 = w31 | (x0_7 << 32);
    let w33: u64 = w32 | (x0_7 << 33);
    let w34: u64 = w33 | (x0_7 << 34);
    let w35: u64 = w34 | (x0_7 << 35);
    let w36: u64 = w35 | (x0_7 << 36);
    let w37: u64 = w36 | (x0_7 << 37);
    let w38: u64 = w37 | (x0_7 << 38);
    let w39: u64 = w38 | (x0_7 << 39);
    let w40: u64 = w39 | (x0_7 << 40);
    let w41: u64 = w40 | (x0_7 << 41);
    let w42: u64 = w41 | (x0_7 << 42);
    let w43: u64 = w42 | (x0_7 << 43);
    let w44: u64 = w43 | (x0_7 << 44);
    let w45: u64 = w44 | (x0_7 << 45);
    let w46: u64 = w45 | (x0_7 << 46);
    let w47: u64 = w46 | (x0_7 << 47);
    let w48: u64 = w47 | (x0_7 << 48);
    let w49: u64 = w48 | (x0_7 << 49);
    let w50: u64 = w49 | (x0_7 << 50);
    let w51: u64 = w50 | (x0_7 << 51);
    let w52: u64 = w51 | (x0_7 << 52);
    let w53: u64 = w52 | (x0_7 << 53);
    let w54: u64 = w53 | (x0_7 << 54);
    let w55: u64 = w54 | (x0_7 << 55);
    let w56: u64 = w55 | (x0_7 << 56);
    let w57: u64 = w56 | (x0_7 << 57);
    let w58: u64 = w57 | (x0_7 << 58);
    let w59: u64 = w58 | (x0_7 << 59);
    let w60: u64 = w59 | (x0_7 << 60);
    let w61: u64 = w60 | (x0_7 << 61);
    let w62: u64 = w61 | (x0_7 << 62);
    let w63: u64 = w62 | (x0_7 << 63);
    ((w63) as u64)
}
