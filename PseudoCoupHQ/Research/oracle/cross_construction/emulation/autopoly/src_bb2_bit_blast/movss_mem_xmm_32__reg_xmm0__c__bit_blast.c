/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of movss_mem_xmm_32__reg_xmm0__c__bit_blast.  The term's text, LITERAL:
   Extract(31, 0, v0) */
#include <stdint.h>
#include <string.h>
static inline float bits_to_f32(uint32_t b) { float f; memcpy(&f, &b, 4); return f; }

float
emu_movss_mem_xmm_32__reg_xmm0__c__bit_blast(uint32_t a)
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
    uint32_t x0_16 = ((uint32_t)(a) >> 16) & 1;
    uint32_t x0_17 = ((uint32_t)(a) >> 17) & 1;
    uint32_t x0_18 = ((uint32_t)(a) >> 18) & 1;
    uint32_t x0_19 = ((uint32_t)(a) >> 19) & 1;
    uint32_t x0_20 = ((uint32_t)(a) >> 20) & 1;
    uint32_t x0_21 = ((uint32_t)(a) >> 21) & 1;
    uint32_t x0_22 = ((uint32_t)(a) >> 22) & 1;
    uint32_t x0_23 = ((uint32_t)(a) >> 23) & 1;
    uint32_t x0_24 = ((uint32_t)(a) >> 24) & 1;
    uint32_t x0_25 = ((uint32_t)(a) >> 25) & 1;
    uint32_t x0_26 = ((uint32_t)(a) >> 26) & 1;
    uint32_t x0_27 = ((uint32_t)(a) >> 27) & 1;
    uint32_t x0_28 = ((uint32_t)(a) >> 28) & 1;
    uint32_t x0_29 = ((uint32_t)(a) >> 29) & 1;
    uint32_t x0_30 = ((uint32_t)(a) >> 30) & 1;
    uint32_t x0_31 = ((uint32_t)(a) >> 31) & 1;
    uint32_t w0 = (x0_0 << 0);
    uint32_t w1 = w0 | (x0_1 << 1);
    uint32_t w2 = w1 | (x0_2 << 2);
    uint32_t w3 = w2 | (x0_3 << 3);
    uint32_t w4 = w3 | (x0_4 << 4);
    uint32_t w5 = w4 | (x0_5 << 5);
    uint32_t w6 = w5 | (x0_6 << 6);
    uint32_t w7 = w6 | (x0_7 << 7);
    uint32_t w8 = w7 | (x0_8 << 8);
    uint32_t w9 = w8 | (x0_9 << 9);
    uint32_t w10 = w9 | (x0_10 << 10);
    uint32_t w11 = w10 | (x0_11 << 11);
    uint32_t w12 = w11 | (x0_12 << 12);
    uint32_t w13 = w12 | (x0_13 << 13);
    uint32_t w14 = w13 | (x0_14 << 14);
    uint32_t w15 = w14 | (x0_15 << 15);
    uint32_t w16 = w15 | (x0_16 << 16);
    uint32_t w17 = w16 | (x0_17 << 17);
    uint32_t w18 = w17 | (x0_18 << 18);
    uint32_t w19 = w18 | (x0_19 << 19);
    uint32_t w20 = w19 | (x0_20 << 20);
    uint32_t w21 = w20 | (x0_21 << 21);
    uint32_t w22 = w21 | (x0_22 << 22);
    uint32_t w23 = w22 | (x0_23 << 23);
    uint32_t w24 = w23 | (x0_24 << 24);
    uint32_t w25 = w24 | (x0_25 << 25);
    uint32_t w26 = w25 | (x0_26 << 26);
    uint32_t w27 = w26 | (x0_27 << 27);
    uint32_t w28 = w27 | (x0_28 << 28);
    uint32_t w29 = w28 | (x0_29 << 29);
    uint32_t w30 = w29 | (x0_30 << 30);
    uint32_t w31 = w30 | (x0_31 << 31);
    return bits_to_f32((uint32_t)(w31));
}
