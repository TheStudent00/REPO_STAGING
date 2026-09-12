#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of movd_gpr_xmm_32__reg_xmm0__rust__bit_blast.
//   Extract(31, 0, v0)
#[no_mangle]
pub extern "C" fn emu_movd_gpr_xmm_32__reg_xmm0__rust__bit_blast(a: u32) -> f32
{
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
    let x0_16: u32 = (((a) as u32) >> 16) & 1;
    let x0_17: u32 = (((a) as u32) >> 17) & 1;
    let x0_18: u32 = (((a) as u32) >> 18) & 1;
    let x0_19: u32 = (((a) as u32) >> 19) & 1;
    let x0_20: u32 = (((a) as u32) >> 20) & 1;
    let x0_21: u32 = (((a) as u32) >> 21) & 1;
    let x0_22: u32 = (((a) as u32) >> 22) & 1;
    let x0_23: u32 = (((a) as u32) >> 23) & 1;
    let x0_24: u32 = (((a) as u32) >> 24) & 1;
    let x0_25: u32 = (((a) as u32) >> 25) & 1;
    let x0_26: u32 = (((a) as u32) >> 26) & 1;
    let x0_27: u32 = (((a) as u32) >> 27) & 1;
    let x0_28: u32 = (((a) as u32) >> 28) & 1;
    let x0_29: u32 = (((a) as u32) >> 29) & 1;
    let x0_30: u32 = (((a) as u32) >> 30) & 1;
    let x0_31: u32 = (((a) as u32) >> 31) & 1;
    let w0: u32 = (x0_0 << 0);
    let w1: u32 = w0 | (x0_1 << 1);
    let w2: u32 = w1 | (x0_2 << 2);
    let w3: u32 = w2 | (x0_3 << 3);
    let w4: u32 = w3 | (x0_4 << 4);
    let w5: u32 = w4 | (x0_5 << 5);
    let w6: u32 = w5 | (x0_6 << 6);
    let w7: u32 = w6 | (x0_7 << 7);
    let w8: u32 = w7 | (x0_8 << 8);
    let w9: u32 = w8 | (x0_9 << 9);
    let w10: u32 = w9 | (x0_10 << 10);
    let w11: u32 = w10 | (x0_11 << 11);
    let w12: u32 = w11 | (x0_12 << 12);
    let w13: u32 = w12 | (x0_13 << 13);
    let w14: u32 = w13 | (x0_14 << 14);
    let w15: u32 = w14 | (x0_15 << 15);
    let w16: u32 = w15 | (x0_16 << 16);
    let w17: u32 = w16 | (x0_17 << 17);
    let w18: u32 = w17 | (x0_18 << 18);
    let w19: u32 = w18 | (x0_19 << 19);
    let w20: u32 = w19 | (x0_20 << 20);
    let w21: u32 = w20 | (x0_21 << 21);
    let w22: u32 = w21 | (x0_22 << 22);
    let w23: u32 = w22 | (x0_23 << 23);
    let w24: u32 = w23 | (x0_24 << 24);
    let w25: u32 = w24 | (x0_25 << 25);
    let w26: u32 = w25 | (x0_26 << 26);
    let w27: u32 = w26 | (x0_27 << 27);
    let w28: u32 = w27 | (x0_28 << 28);
    let w29: u32 = w28 | (x0_29 << 29);
    let w30: u32 = w29 | (x0_30 << 30);
    let w31: u32 = w30 | (x0_31 << 31);
    f32::from_bits((w31) as u32)
}
