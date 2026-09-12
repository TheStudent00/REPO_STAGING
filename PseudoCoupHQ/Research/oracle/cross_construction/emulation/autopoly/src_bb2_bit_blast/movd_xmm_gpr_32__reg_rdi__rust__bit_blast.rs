#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of movd_xmm_gpr_32__reg_rdi__rust__bit_blast.
//   Concat(0, Extract(31, 0, v0))
#[no_mangle]
pub extern "C" fn emu_movd_xmm_gpr_32__reg_rdi__rust__bit_blast(a: f32) -> u64
{
    let x0_0: u64 = (((a) as u64) >> 0) & 1;
    let x0_1: u64 = (((a) as u64) >> 1) & 1;
    let x0_2: u64 = (((a) as u64) >> 2) & 1;
    let x0_3: u64 = (((a) as u64) >> 3) & 1;
    let x0_4: u64 = (((a) as u64) >> 4) & 1;
    let x0_5: u64 = (((a) as u64) >> 5) & 1;
    let x0_6: u64 = (((a) as u64) >> 6) & 1;
    let x0_7: u64 = (((a) as u64) >> 7) & 1;
    let x0_8: u64 = (((a) as u64) >> 8) & 1;
    let x0_9: u64 = (((a) as u64) >> 9) & 1;
    let x0_10: u64 = (((a) as u64) >> 10) & 1;
    let x0_11: u64 = (((a) as u64) >> 11) & 1;
    let x0_12: u64 = (((a) as u64) >> 12) & 1;
    let x0_13: u64 = (((a) as u64) >> 13) & 1;
    let x0_14: u64 = (((a) as u64) >> 14) & 1;
    let x0_15: u64 = (((a) as u64) >> 15) & 1;
    let x0_16: u64 = (((a) as u64) >> 16) & 1;
    let x0_17: u64 = (((a) as u64) >> 17) & 1;
    let x0_18: u64 = (((a) as u64) >> 18) & 1;
    let x0_19: u64 = (((a) as u64) >> 19) & 1;
    let x0_20: u64 = (((a) as u64) >> 20) & 1;
    let x0_21: u64 = (((a) as u64) >> 21) & 1;
    let x0_22: u64 = (((a) as u64) >> 22) & 1;
    let x0_23: u64 = (((a) as u64) >> 23) & 1;
    let x0_24: u64 = (((a) as u64) >> 24) & 1;
    let x0_25: u64 = (((a) as u64) >> 25) & 1;
    let x0_26: u64 = (((a) as u64) >> 26) & 1;
    let x0_27: u64 = (((a) as u64) >> 27) & 1;
    let x0_28: u64 = (((a) as u64) >> 28) & 1;
    let x0_29: u64 = (((a) as u64) >> 29) & 1;
    let x0_30: u64 = (((a) as u64) >> 30) & 1;
    let x0_31: u64 = (((a) as u64) >> 31) & 1;
    let k0: u64 = 0;
    let w0: u64 = (x0_0 << 0);
    let w1: u64 = w0 | (x0_1 << 1);
    let w2: u64 = w1 | (x0_2 << 2);
    let w3: u64 = w2 | (x0_3 << 3);
    let w4: u64 = w3 | (x0_4 << 4);
    let w5: u64 = w4 | (x0_5 << 5);
    let w6: u64 = w5 | (x0_6 << 6);
    let w7: u64 = w6 | (x0_7 << 7);
    let w8: u64 = w7 | (x0_8 << 8);
    let w9: u64 = w8 | (x0_9 << 9);
    let w10: u64 = w9 | (x0_10 << 10);
    let w11: u64 = w10 | (x0_11 << 11);
    let w12: u64 = w11 | (x0_12 << 12);
    let w13: u64 = w12 | (x0_13 << 13);
    let w14: u64 = w13 | (x0_14 << 14);
    let w15: u64 = w14 | (x0_15 << 15);
    let w16: u64 = w15 | (x0_16 << 16);
    let w17: u64 = w16 | (x0_17 << 17);
    let w18: u64 = w17 | (x0_18 << 18);
    let w19: u64 = w18 | (x0_19 << 19);
    let w20: u64 = w19 | (x0_20 << 20);
    let w21: u64 = w20 | (x0_21 << 21);
    let w22: u64 = w21 | (x0_22 << 22);
    let w23: u64 = w22 | (x0_23 << 23);
    let w24: u64 = w23 | (x0_24 << 24);
    let w25: u64 = w24 | (x0_25 << 25);
    let w26: u64 = w25 | (x0_26 << 26);
    let w27: u64 = w26 | (x0_27 << 27);
    let w28: u64 = w27 | (x0_28 << 28);
    let w29: u64 = w28 | (x0_29 << 29);
    let w30: u64 = w29 | (x0_30 << 30);
    let w31: u64 = w30 | (x0_31 << 31);
    let w32: u64 = w31 | (k0 << 32);
    let w33: u64 = w32 | (k0 << 33);
    let w34: u64 = w33 | (k0 << 34);
    let w35: u64 = w34 | (k0 << 35);
    let w36: u64 = w35 | (k0 << 36);
    let w37: u64 = w36 | (k0 << 37);
    let w38: u64 = w37 | (k0 << 38);
    let w39: u64 = w38 | (k0 << 39);
    let w40: u64 = w39 | (k0 << 40);
    let w41: u64 = w40 | (k0 << 41);
    let w42: u64 = w41 | (k0 << 42);
    let w43: u64 = w42 | (k0 << 43);
    let w44: u64 = w43 | (k0 << 44);
    let w45: u64 = w44 | (k0 << 45);
    let w46: u64 = w45 | (k0 << 46);
    let w47: u64 = w46 | (k0 << 47);
    let w48: u64 = w47 | (k0 << 48);
    let w49: u64 = w48 | (k0 << 49);
    let w50: u64 = w49 | (k0 << 50);
    let w51: u64 = w50 | (k0 << 51);
    let w52: u64 = w51 | (k0 << 52);
    let w53: u64 = w52 | (k0 << 53);
    let w54: u64 = w53 | (k0 << 54);
    let w55: u64 = w54 | (k0 << 55);
    let w56: u64 = w55 | (k0 << 56);
    let w57: u64 = w56 | (k0 << 57);
    let w58: u64 = w57 | (k0 << 58);
    let w59: u64 = w58 | (k0 << 59);
    let w60: u64 = w59 | (k0 << 60);
    let w61: u64 = w60 | (k0 << 61);
    let w62: u64 = w61 | (k0 << 62);
    let w63: u64 = w62 | (k0 << 63);
    ((w63) as u64)
}
