/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of pextrw_imm_xmm_gpr_128__reg_rdi__cpp__bit_blast.  The term's text, LITERAL:
   Concat(0, Extract(31, 16, v0)) */
#include <cstdint>

extern "C"
uint64_t
emu_pextrw_imm_xmm_gpr_128__reg_rdi__cpp__bit_blast(float a)
{
    uint64_t x0_16 = ((uint64_t)(a) >> 16) & 1;
    uint64_t x0_17 = ((uint64_t)(a) >> 17) & 1;
    uint64_t x0_18 = ((uint64_t)(a) >> 18) & 1;
    uint64_t x0_19 = ((uint64_t)(a) >> 19) & 1;
    uint64_t x0_20 = ((uint64_t)(a) >> 20) & 1;
    uint64_t x0_21 = ((uint64_t)(a) >> 21) & 1;
    uint64_t x0_22 = ((uint64_t)(a) >> 22) & 1;
    uint64_t x0_23 = ((uint64_t)(a) >> 23) & 1;
    uint64_t x0_24 = ((uint64_t)(a) >> 24) & 1;
    uint64_t x0_25 = ((uint64_t)(a) >> 25) & 1;
    uint64_t x0_26 = ((uint64_t)(a) >> 26) & 1;
    uint64_t x0_27 = ((uint64_t)(a) >> 27) & 1;
    uint64_t x0_28 = ((uint64_t)(a) >> 28) & 1;
    uint64_t x0_29 = ((uint64_t)(a) >> 29) & 1;
    uint64_t x0_30 = ((uint64_t)(a) >> 30) & 1;
    uint64_t x0_31 = ((uint64_t)(a) >> 31) & 1;
    uint64_t k0 = 0;
    uint64_t w0 = (x0_16 << 0);
    uint64_t w1 = w0 | (x0_17 << 1);
    uint64_t w2 = w1 | (x0_18 << 2);
    uint64_t w3 = w2 | (x0_19 << 3);
    uint64_t w4 = w3 | (x0_20 << 4);
    uint64_t w5 = w4 | (x0_21 << 5);
    uint64_t w6 = w5 | (x0_22 << 6);
    uint64_t w7 = w6 | (x0_23 << 7);
    uint64_t w8 = w7 | (x0_24 << 8);
    uint64_t w9 = w8 | (x0_25 << 9);
    uint64_t w10 = w9 | (x0_26 << 10);
    uint64_t w11 = w10 | (x0_27 << 11);
    uint64_t w12 = w11 | (x0_28 << 12);
    uint64_t w13 = w12 | (x0_29 << 13);
    uint64_t w14 = w13 | (x0_30 << 14);
    uint64_t w15 = w14 | (x0_31 << 15);
    uint64_t w16 = w15 | (k0 << 16);
    uint64_t w17 = w16 | (k0 << 17);
    uint64_t w18 = w17 | (k0 << 18);
    uint64_t w19 = w18 | (k0 << 19);
    uint64_t w20 = w19 | (k0 << 20);
    uint64_t w21 = w20 | (k0 << 21);
    uint64_t w22 = w21 | (k0 << 22);
    uint64_t w23 = w22 | (k0 << 23);
    uint64_t w24 = w23 | (k0 << 24);
    uint64_t w25 = w24 | (k0 << 25);
    uint64_t w26 = w25 | (k0 << 26);
    uint64_t w27 = w26 | (k0 << 27);
    uint64_t w28 = w27 | (k0 << 28);
    uint64_t w29 = w28 | (k0 << 29);
    uint64_t w30 = w29 | (k0 << 30);
    uint64_t w31 = w30 | (k0 << 31);
    uint64_t w32 = w31 | (k0 << 32);
    uint64_t w33 = w32 | (k0 << 33);
    uint64_t w34 = w33 | (k0 << 34);
    uint64_t w35 = w34 | (k0 << 35);
    uint64_t w36 = w35 | (k0 << 36);
    uint64_t w37 = w36 | (k0 << 37);
    uint64_t w38 = w37 | (k0 << 38);
    uint64_t w39 = w38 | (k0 << 39);
    uint64_t w40 = w39 | (k0 << 40);
    uint64_t w41 = w40 | (k0 << 41);
    uint64_t w42 = w41 | (k0 << 42);
    uint64_t w43 = w42 | (k0 << 43);
    uint64_t w44 = w43 | (k0 << 44);
    uint64_t w45 = w44 | (k0 << 45);
    uint64_t w46 = w45 | (k0 << 46);
    uint64_t w47 = w46 | (k0 << 47);
    uint64_t w48 = w47 | (k0 << 48);
    uint64_t w49 = w48 | (k0 << 49);
    uint64_t w50 = w49 | (k0 << 50);
    uint64_t w51 = w50 | (k0 << 51);
    uint64_t w52 = w51 | (k0 << 52);
    uint64_t w53 = w52 | (k0 << 53);
    uint64_t w54 = w53 | (k0 << 54);
    uint64_t w55 = w54 | (k0 << 55);
    uint64_t w56 = w55 | (k0 << 56);
    uint64_t w57 = w56 | (k0 << 57);
    uint64_t w58 = w57 | (k0 << 58);
    uint64_t w59 = w58 | (k0 << 59);
    uint64_t w60 = w59 | (k0 << 60);
    uint64_t w61 = w60 | (k0 << 61);
    uint64_t w62 = w61 | (k0 << 62);
    uint64_t w63 = w62 | (k0 << 63);
    return (uint64_t)(w63);
}
