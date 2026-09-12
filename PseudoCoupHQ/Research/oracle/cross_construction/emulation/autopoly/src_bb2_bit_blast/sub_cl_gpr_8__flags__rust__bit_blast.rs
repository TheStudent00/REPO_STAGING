#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]
#![allow(unused_variables, unused_mut)]

// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of sub_cl_gpr_8__flags__rust__bit_blast.
//   Concat(Extract(7, 0, v0), Extract(7, 0, v1))
#[no_mangle]
pub extern "C" fn emu_sub_cl_gpr_8__flags__rust__bit_blast(a: u8, b: u8) -> u16
{
    let x1_0: u32 = (((b) as u32) >> 0) & 1;
    let x1_1: u32 = (((b) as u32) >> 1) & 1;
    let x1_2: u32 = (((b) as u32) >> 2) & 1;
    let x1_3: u32 = (((b) as u32) >> 3) & 1;
    let x1_4: u32 = (((b) as u32) >> 4) & 1;
    let x1_5: u32 = (((b) as u32) >> 5) & 1;
    let x1_6: u32 = (((b) as u32) >> 6) & 1;
    let x1_7: u32 = (((b) as u32) >> 7) & 1;
    let x0_0: u32 = (((a) as u32) >> 0) & 1;
    let x0_1: u32 = (((a) as u32) >> 1) & 1;
    let x0_2: u32 = (((a) as u32) >> 2) & 1;
    let x0_3: u32 = (((a) as u32) >> 3) & 1;
    let x0_4: u32 = (((a) as u32) >> 4) & 1;
    let x0_5: u32 = (((a) as u32) >> 5) & 1;
    let x0_6: u32 = (((a) as u32) >> 6) & 1;
    let x0_7: u32 = (((a) as u32) >> 7) & 1;
    let w0: u32 = (x1_0 << 0);
    let w1: u32 = w0 | (x1_1 << 1);
    let w2: u32 = w1 | (x1_2 << 2);
    let w3: u32 = w2 | (x1_3 << 3);
    let w4: u32 = w3 | (x1_4 << 4);
    let w5: u32 = w4 | (x1_5 << 5);
    let w6: u32 = w5 | (x1_6 << 6);
    let w7: u32 = w6 | (x1_7 << 7);
    let w8: u32 = w7 | (x0_0 << 8);
    let w9: u32 = w8 | (x0_1 << 9);
    let w10: u32 = w9 | (x0_2 << 10);
    let w11: u32 = w10 | (x0_3 << 11);
    let w12: u32 = w11 | (x0_4 << 12);
    let w13: u32 = w12 | (x0_5 << 13);
    let w14: u32 = w13 | (x0_6 << 14);
    let w15: u32 = w14 | (x0_7 << 15);
    ((w15) as u16)
}
