/* sfemul_altpin.h - the OPPOSITE reading of every don't-care in the flattened
 * IR, used only by scripts/pin_probe.sh.  Nothing in emulations/ includes it.
 *
 * The flattened block contains shifts whose amount can exceed the operand
 * width, a ctlz whose operand can be zero, and a udiv whose divisor the
 * flattener has already forced non-zero.  LLVM calls all three poison and the
 * flattener puts a `freeze` on each, which says the value is arbitrary but
 * fixed.  emulations/ pins them one way; this header pins them the other way,
 * and the same SoftFloat test is run against the result.  If both agree with
 * SoftFloat on every input, the pins are unobservable, not lucky.
 *
 *   shift amount >= width   ->  0            (emulations: amount mod width)
 *   ctlz(0)                 ->  0            (emulations: the bit width)
 *   udiv by zero            ->  all ones     (emulations: zero)
 */
#ifndef SFEMUL_ALTPIN_H
#define SFEMUL_ALTPIN_H

#include "sfemul.h"

#define SF_ALT_SHIFT(NAME, T, W, OP)                                    \
    static inline T NAME(T a, T b)                                      \
    {                                                                   \
        return (b >= (T)W) ? (T)0 : (T)((T)a OP (unsigned)b);           \
    }

SF_ALT_SHIFT(sf_shl8_alt, uint8_t, 8, <<)
SF_ALT_SHIFT(sf_shl16_alt, uint16_t, 16, <<)
SF_ALT_SHIFT(sf_shl32_alt, uint32_t, 32, <<)
SF_ALT_SHIFT(sf_shl64_alt, uint64_t, 64, <<)
SF_ALT_SHIFT(sf_lshr8_alt, uint8_t, 8, >>)
SF_ALT_SHIFT(sf_lshr16_alt, uint16_t, 16, >>)
SF_ALT_SHIFT(sf_lshr32_alt, uint32_t, 32, >>)
SF_ALT_SHIFT(sf_lshr64_alt, uint64_t, 64, >>)

static inline sf_u128 sf_shl128_alt(sf_u128 a, sf_u128 b)
{
    return (b >= 128) ? (sf_u128)0 : (sf_u128)(a << (unsigned)b);
}
static inline sf_u128 sf_lshr128_alt(sf_u128 a, sf_u128 b)
{
    return (b >= 128) ? (sf_u128)0 : (sf_u128)(a >> (unsigned)b);
}

static inline uint32_t sf_ctlz32_alt(uint32_t x)
{
    return x ? sf_ctlz32(x) : UINT32_C(0);
}
static inline uint64_t sf_ctlz64_alt(uint64_t x)
{
    return x ? sf_ctlz64(x) : UINT64_C(0);
}

static inline uint32_t sf_udiv32_alt(uint32_t a, uint32_t b)
{
    return b ? (a / b) : UINT32_C(0xFFFFFFFF);
}
static inline uint64_t sf_udiv64_alt(uint64_t a, uint64_t b)
{
    return b ? (a / b) : ~UINT64_C(0);
}
static inline sf_u128 sf_u128_udiv_alt(sf_u128 a, sf_u128 b)
{
    return b ? (a / b) : (sf_u128)0 - (sf_u128)1;
}

#endif /* SFEMUL_ALTPIN_H */
