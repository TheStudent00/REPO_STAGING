/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of imul_gpr_gpr_16__flags__c__bit_blast.  The term's text, LITERAL:
   Concat(Extract(15, 0, v0), Extract(15, 0, v1)) */
#include <stdint.h>

uint32_t
emu_imul_gpr_gpr_16__flags__c__bit_blast(uint16_t a, uint16_t b)
{
    uint32_t x1_0 = ((uint32_t)(b) >> 0) & 1;
    uint32_t x1_1 = ((uint32_t)(b) >> 1) & 1;
    uint32_t x1_2 = ((uint32_t)(b) >> 2) & 1;
    uint32_t x1_3 = ((uint32_t)(b) >> 3) & 1;
    uint32_t x1_4 = ((uint32_t)(b) >> 4) & 1;
    uint32_t x1_5 = ((uint32_t)(b) >> 5) & 1;
    uint32_t x1_6 = ((uint32_t)(b) >> 6) & 1;
    uint32_t x1_7 = ((uint32_t)(b) >> 7) & 1;
    uint32_t x1_8 = ((uint32_t)(b) >> 8) & 1;
    uint32_t x1_9 = ((uint32_t)(b) >> 9) & 1;
    uint32_t x1_10 = ((uint32_t)(b) >> 10) & 1;
    uint32_t x1_11 = ((uint32_t)(b) >> 11) & 1;
    uint32_t x1_12 = ((uint32_t)(b) >> 12) & 1;
    uint32_t x1_13 = ((uint32_t)(b) >> 13) & 1;
    uint32_t x1_14 = ((uint32_t)(b) >> 14) & 1;
    uint32_t x1_15 = ((uint32_t)(b) >> 15) & 1;
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
    uint32_t w0 = (x1_0 << 0);
    uint32_t w1 = w0 | (x1_1 << 1);
    uint32_t w2 = w1 | (x1_2 << 2);
    uint32_t w3 = w2 | (x1_3 << 3);
    uint32_t w4 = w3 | (x1_4 << 4);
    uint32_t w5 = w4 | (x1_5 << 5);
    uint32_t w6 = w5 | (x1_6 << 6);
    uint32_t w7 = w6 | (x1_7 << 7);
    uint32_t w8 = w7 | (x1_8 << 8);
    uint32_t w9 = w8 | (x1_9 << 9);
    uint32_t w10 = w9 | (x1_10 << 10);
    uint32_t w11 = w10 | (x1_11 << 11);
    uint32_t w12 = w11 | (x1_12 << 12);
    uint32_t w13 = w12 | (x1_13 << 13);
    uint32_t w14 = w13 | (x1_14 << 14);
    uint32_t w15 = w14 | (x1_15 << 15);
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
