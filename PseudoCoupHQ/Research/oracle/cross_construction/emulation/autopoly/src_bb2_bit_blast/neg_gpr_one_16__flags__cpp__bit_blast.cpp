/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of neg_gpr_one_16__flags__cpp__bit_blast.  The term's text, LITERAL:
   Concat(Extract(15, 0, v0), 0) */
#include <cstdint>

extern "C"
uint32_t
emu_neg_gpr_one_16__flags__cpp__bit_blast(uint16_t a)
{
    uint32_t x0_0 = ((uint32_t)(a) >> 0) & 1;
    uint32_t x0_1 = ((uint32_t)(a) >> 1) & 1;
    uint32_t x0_2 = ((uint32_t)(a) >> 2) & 1;
    uint32_t x0_3 = ((uint32_t)(a) >> 3) & 1;
    uint32_t x0_4 = ((uint32_t)(a) >> 4) & 1;
    uint32_t x0_5 = ((uint32_t)(a) >> 5) & 1;
    uint32_t x0_6 = ((uint32_t)(a) >> 6) & 1;
    uint32_t x0_7 = ((uint32_t)(a) >> 7) & 1;
    uint32_t x0_8 = ((uint32_t)(a) >> 8) & 1;
    uint32_t x0_9 = ((uint32_t)(a) >> 9) & 1;
    uint32_t x0_10 = ((uint32_t)(a) >> 10) & 1;
    uint32_t x0_11 = ((uint32_t)(a) >> 11) & 1;
    uint32_t x0_12 = ((uint32_t)(a) >> 12) & 1;
    uint32_t x0_13 = ((uint32_t)(a) >> 13) & 1;
    uint32_t x0_14 = ((uint32_t)(a) >> 14) & 1;
    uint32_t x0_15 = ((uint32_t)(a) >> 15) & 1;
    uint32_t k0 = 0;
    uint32_t w0 = (k0 << 0);
    uint32_t w1 = w0 | (k0 << 1);
    uint32_t w2 = w1 | (k0 << 2);
    uint32_t w3 = w2 | (k0 << 3);
    uint32_t w4 = w3 | (k0 << 4);
    uint32_t w5 = w4 | (k0 << 5);
    uint32_t w6 = w5 | (k0 << 6);
    uint32_t w7 = w6 | (k0 << 7);
    uint32_t w8 = w7 | (k0 << 8);
    uint32_t w9 = w8 | (k0 << 9);
    uint32_t w10 = w9 | (k0 << 10);
    uint32_t w11 = w10 | (k0 << 11);
    uint32_t w12 = w11 | (k0 << 12);
    uint32_t w13 = w12 | (k0 << 13);
    uint32_t w14 = w13 | (k0 << 14);
    uint32_t w15 = w14 | (k0 << 15);
    uint32_t w16 = w15 | (x0_0 << 16);
    uint32_t w17 = w16 | (x0_1 << 17);
    uint32_t w18 = w17 | (x0_2 << 18);
    uint32_t w19 = w18 | (x0_3 << 19);
    uint32_t w20 = w19 | (x0_4 << 20);
    uint32_t w21 = w20 | (x0_5 << 21);
    uint32_t w22 = w21 | (x0_6 << 22);
    uint32_t w23 = w22 | (x0_7 << 23);
    uint32_t w24 = w23 | (x0_8 << 24);
    uint32_t w25 = w24 | (x0_9 << 25);
    uint32_t w26 = w25 | (x0_10 << 26);
    uint32_t w27 = w26 | (x0_11 << 27);
    uint32_t w28 = w27 | (x0_12 << 28);
    uint32_t w29 = w28 | (x0_13 << 29);
    uint32_t w30 = w29 | (x0_14 << 30);
    uint32_t w31 = w30 | (x0_15 << 31);
    return (uint32_t)(w31);
}
