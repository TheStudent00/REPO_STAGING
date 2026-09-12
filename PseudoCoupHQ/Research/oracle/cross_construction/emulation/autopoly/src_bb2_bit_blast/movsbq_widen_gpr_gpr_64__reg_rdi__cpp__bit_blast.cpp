/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of movsbq_widen_gpr_gpr_64__reg_rdi__cpp__bit_blast.  The term's text, LITERAL:
   Concat(Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0),  */
#include <cstdint>

extern "C"
uint64_t
emu_movsbq_widen_gpr_gpr_64__reg_rdi__cpp__bit_blast(uint8_t a)
{
    uint64_t x0_0 = ((uint64_t)(a) >> 0) & 1;
    uint64_t x0_1 = ((uint64_t)(a) >> 1) & 1;
    uint64_t x0_2 = ((uint64_t)(a) >> 2) & 1;
    uint64_t x0_3 = ((uint64_t)(a) >> 3) & 1;
    uint64_t x0_4 = ((uint64_t)(a) >> 4) & 1;
    uint64_t x0_5 = ((uint64_t)(a) >> 5) & 1;
    uint64_t x0_6 = ((uint64_t)(a) >> 6) & 1;
    uint64_t x0_7 = ((uint64_t)(a) >> 7) & 1;
    uint64_t w0 = (x0_0 << 0);
    uint64_t w1 = w0 | (x0_1 << 1);
    uint64_t w2 = w1 | (x0_2 << 2);
    uint64_t w3 = w2 | (x0_3 << 3);
    uint64_t w4 = w3 | (x0_4 << 4);
    uint64_t w5 = w4 | (x0_5 << 5);
    uint64_t w6 = w5 | (x0_6 << 6);
    uint64_t w7 = w6 | (x0_7 << 7);
    uint64_t w8 = w7 | (x0_7 << 8);
    uint64_t w9 = w8 | (x0_7 << 9);
    uint64_t w10 = w9 | (x0_7 << 10);
    uint64_t w11 = w10 | (x0_7 << 11);
    uint64_t w12 = w11 | (x0_7 << 12);
    uint64_t w13 = w12 | (x0_7 << 13);
    uint64_t w14 = w13 | (x0_7 << 14);
    uint64_t w15 = w14 | (x0_7 << 15);
    uint64_t w16 = w15 | (x0_7 << 16);
    uint64_t w17 = w16 | (x0_7 << 17);
    uint64_t w18 = w17 | (x0_7 << 18);
    uint64_t w19 = w18 | (x0_7 << 19);
    uint64_t w20 = w19 | (x0_7 << 20);
    uint64_t w21 = w20 | (x0_7 << 21);
    uint64_t w22 = w21 | (x0_7 << 22);
    uint64_t w23 = w22 | (x0_7 << 23);
    uint64_t w24 = w23 | (x0_7 << 24);
    uint64_t w25 = w24 | (x0_7 << 25);
    uint64_t w26 = w25 | (x0_7 << 26);
    uint64_t w27 = w26 | (x0_7 << 27);
    uint64_t w28 = w27 | (x0_7 << 28);
    uint64_t w29 = w28 | (x0_7 << 29);
    uint64_t w30 = w29 | (x0_7 << 30);
    uint64_t w31 = w30 | (x0_7 << 31);
    uint64_t w32 = w31 | (x0_7 << 32);
    uint64_t w33 = w32 | (x0_7 << 33);
    uint64_t w34 = w33 | (x0_7 << 34);
    uint64_t w35 = w34 | (x0_7 << 35);
    uint64_t w36 = w35 | (x0_7 << 36);
    uint64_t w37 = w36 | (x0_7 << 37);
    uint64_t w38 = w37 | (x0_7 << 38);
    uint64_t w39 = w38 | (x0_7 << 39);
    uint64_t w40 = w39 | (x0_7 << 40);
    uint64_t w41 = w40 | (x0_7 << 41);
    uint64_t w42 = w41 | (x0_7 << 42);
    uint64_t w43 = w42 | (x0_7 << 43);
    uint64_t w44 = w43 | (x0_7 << 44);
    uint64_t w45 = w44 | (x0_7 << 45);
    uint64_t w46 = w45 | (x0_7 << 46);
    uint64_t w47 = w46 | (x0_7 << 47);
    uint64_t w48 = w47 | (x0_7 << 48);
    uint64_t w49 = w48 | (x0_7 << 49);
    uint64_t w50 = w49 | (x0_7 << 50);
    uint64_t w51 = w50 | (x0_7 << 51);
    uint64_t w52 = w51 | (x0_7 << 52);
    uint64_t w53 = w52 | (x0_7 << 53);
    uint64_t w54 = w53 | (x0_7 << 54);
    uint64_t w55 = w54 | (x0_7 << 55);
    uint64_t w56 = w55 | (x0_7 << 56);
    uint64_t w57 = w56 | (x0_7 << 57);
    uint64_t w58 = w57 | (x0_7 << 58);
    uint64_t w59 = w58 | (x0_7 << 59);
    uint64_t w60 = w59 | (x0_7 << 60);
    uint64_t w61 = w60 | (x0_7 << 61);
    uint64_t w62 = w61 | (x0_7 << 62);
    uint64_t w63 = w62 | (x0_7 << 63);
    return (uint64_t)(w63);
}
