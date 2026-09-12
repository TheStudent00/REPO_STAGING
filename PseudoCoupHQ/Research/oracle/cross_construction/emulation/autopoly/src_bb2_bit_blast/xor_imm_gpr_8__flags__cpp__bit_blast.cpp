/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of xor_imm_gpr_8__flags__cpp__bit_blast.  The term's text, LITERAL:
   Concat(Extract(7, 0, v0) ^ Extract(7, 0, v1), 0) */
#include <cstdint>

extern "C"
uint16_t
emu_xor_imm_gpr_8__flags__cpp__bit_blast(uint8_t a, uint8_t b)
{
    uint32_t x1_0 = ((uint32_t)(a) >> 0) & 1;
    uint32_t x0_0 = ((uint32_t)(b) >> 0) & 1;
    uint32_t x1_1 = ((uint32_t)(a) >> 1) & 1;
    uint32_t x0_1 = ((uint32_t)(b) >> 1) & 1;
    uint32_t x1_2 = ((uint32_t)(a) >> 2) & 1;
    uint32_t x0_2 = ((uint32_t)(b) >> 2) & 1;
    uint32_t x1_3 = ((uint32_t)(a) >> 3) & 1;
    uint32_t x0_3 = ((uint32_t)(b) >> 3) & 1;
    uint32_t x1_4 = ((uint32_t)(a) >> 4) & 1;
    uint32_t x0_4 = ((uint32_t)(b) >> 4) & 1;
    uint32_t x1_5 = ((uint32_t)(a) >> 5) & 1;
    uint32_t x0_5 = ((uint32_t)(b) >> 5) & 1;
    uint32_t x1_6 = ((uint32_t)(a) >> 6) & 1;
    uint32_t x0_6 = ((uint32_t)(b) >> 6) & 1;
    uint32_t x1_7 = ((uint32_t)(a) >> 7) & 1;
    uint32_t x0_7 = ((uint32_t)(b) >> 7) & 1;
    uint32_t k0 = 0;
    uint32_t g0 = (x0_0 ^ x1_0);
    uint32_t g1 = (g0 ^ 1);
    uint32_t g2 = (g1 ^ 1);
    uint32_t g3 = (x0_1 ^ x1_1);
    uint32_t g4 = (g3 ^ 1);
    uint32_t g5 = (g4 ^ 1);
    uint32_t g6 = (x0_2 ^ x1_2);
    uint32_t g7 = (g6 ^ 1);
    uint32_t g8 = (g7 ^ 1);
    uint32_t g9 = (x0_3 ^ x1_3);
    uint32_t g10 = (g9 ^ 1);
    uint32_t g11 = (g10 ^ 1);
    uint32_t g12 = (x0_4 ^ x1_4);
    uint32_t g13 = (g12 ^ 1);
    uint32_t g14 = (g13 ^ 1);
    uint32_t g15 = (x0_5 ^ x1_5);
    uint32_t g16 = (g15 ^ 1);
    uint32_t g17 = (g16 ^ 1);
    uint32_t g18 = (x0_6 ^ x1_6);
    uint32_t g19 = (g18 ^ 1);
    uint32_t g20 = (g19 ^ 1);
    uint32_t g21 = (x0_7 ^ x1_7);
    uint32_t g22 = (g21 ^ 1);
    uint32_t g23 = (g22 ^ 1);
    uint32_t w0 = (k0 << 0);
    uint32_t w1 = w0 | (k0 << 1);
    uint32_t w2 = w1 | (k0 << 2);
    uint32_t w3 = w2 | (k0 << 3);
    uint32_t w4 = w3 | (k0 << 4);
    uint32_t w5 = w4 | (k0 << 5);
    uint32_t w6 = w5 | (k0 << 6);
    uint32_t w7 = w6 | (k0 << 7);
    uint32_t w8 = w7 | (g2 << 8);
    uint32_t w9 = w8 | (g5 << 9);
    uint32_t w10 = w9 | (g8 << 10);
    uint32_t w11 = w10 | (g11 << 11);
    uint32_t w12 = w11 | (g14 << 12);
    uint32_t w13 = w12 | (g17 << 13);
    uint32_t w14 = w13 | (g20 << 14);
    uint32_t w15 = w14 | (g23 << 15);
    return (uint16_t)(w15);
}
