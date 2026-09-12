/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of sub_cl_gpr_8__flags__cpp__bit_blast.  The term's text, LITERAL:
   Concat(Extract(7, 0, v0), Extract(7, 0, v1)) */
#include <cstdint>

extern "C"
uint16_t
emu_sub_cl_gpr_8__flags__cpp__bit_blast(uint8_t a, uint8_t b)
{
    uint32_t x1_0 = ((uint32_t)(b) >> 0) & 1;
    uint32_t x1_1 = ((uint32_t)(b) >> 1) & 1;
    uint32_t x1_2 = ((uint32_t)(b) >> 2) & 1;
    uint32_t x1_3 = ((uint32_t)(b) >> 3) & 1;
    uint32_t x1_4 = ((uint32_t)(b) >> 4) & 1;
    uint32_t x1_5 = ((uint32_t)(b) >> 5) & 1;
    uint32_t x1_6 = ((uint32_t)(b) >> 6) & 1;
    uint32_t x1_7 = ((uint32_t)(b) >> 7) & 1;
    uint32_t x0_0 = ((uint32_t)(a) >> 0) & 1;
    uint32_t x0_1 = ((uint32_t)(a) >> 1) & 1;
    uint32_t x0_2 = ((uint32_t)(a) >> 2) & 1;
    uint32_t x0_3 = ((uint32_t)(a) >> 3) & 1;
    uint32_t x0_4 = ((uint32_t)(a) >> 4) & 1;
    uint32_t x0_5 = ((uint32_t)(a) >> 5) & 1;
    uint32_t x0_6 = ((uint32_t)(a) >> 6) & 1;
    uint32_t x0_7 = ((uint32_t)(a) >> 7) & 1;
    uint32_t w0 = (x1_0 << 0);
    uint32_t w1 = w0 | (x1_1 << 1);
    uint32_t w2 = w1 | (x1_2 << 2);
    uint32_t w3 = w2 | (x1_3 << 3);
    uint32_t w4 = w3 | (x1_4 << 4);
    uint32_t w5 = w4 | (x1_5 << 5);
    uint32_t w6 = w5 | (x1_6 << 6);
    uint32_t w7 = w6 | (x1_7 << 7);
    uint32_t w8 = w7 | (x0_0 << 8);
    uint32_t w9 = w8 | (x0_1 << 9);
    uint32_t w10 = w9 | (x0_2 << 10);
    uint32_t w11 = w10 | (x0_3 << 11);
    uint32_t w12 = w11 | (x0_4 << 12);
    uint32_t w13 = w12 | (x0_5 << 13);
    uint32_t w14 = w13 | (x0_6 << 14);
    uint32_t w15 = w14 | (x0_7 << 15);
    return (uint16_t)(w15);
}
