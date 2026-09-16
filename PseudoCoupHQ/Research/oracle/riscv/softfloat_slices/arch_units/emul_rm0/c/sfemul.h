/* sfemul.h - the eight LLVM intrinsics the flattened slices use, plus the
 * three don't-care pins, written once for C and reused by every operation.
 *
 * ctlz       WRITTEN OUT.  __builtin_clz(0) is undefined; LLVM's ctlz here
 *            must answer the bit width (see emulations/README.md).
 * abs        WRITTEN OUT.  C's abs() is int-only and undefined at INT_MIN;
 *            LLVM's llvm.abs with is_int_min_poison=false wraps to INT_MIN.
 * usub.sat   WRITTEN OUT.  C has no saturating subtract.
 * fshl       WRITTEN OUT.  C has no funnel shift.
 * udiv       WRITTEN OUT with a zero guard; the flattener already forces
 *            every divisor non-zero, the guard only keeps the program total.
 */
#ifndef SFEMUL_H
#define SFEMUL_H

#include <stdint.h>
#include <stdbool.h>

typedef unsigned __int128 sf_u128;
typedef signed __int128 sf_i128;

/* ---------------------------------------------------------- intrinsics -- */

static inline uint32_t sf_ctlz32(uint32_t x)
{
    uint32_t n = 0;
    if (x == 0) return 32;
    if (!(x & UINT32_C(0xFFFF0000))) { n += 16; x <<= 16; }
    if (!(x & UINT32_C(0xFF000000))) { n += 8;  x <<= 8;  }
    if (!(x & UINT32_C(0xF0000000))) { n += 4;  x <<= 4;  }
    if (!(x & UINT32_C(0xC0000000))) { n += 2;  x <<= 2;  }
    if (!(x & UINT32_C(0x80000000))) { n += 1; }
    return n;
}

static inline uint64_t sf_ctlz64(uint64_t x)
{
    if (x == 0) return 64;
    if (x >> 32) return sf_ctlz32((uint32_t)(x >> 32));
    return 32 + sf_ctlz32((uint32_t)x);
}

static inline uint16_t sf_abs16(uint16_t x)
{
    return ((int16_t)x < 0) ? (uint16_t)(UINT16_C(0) - x) : x;
}

static inline uint32_t sf_abs32(uint32_t x)
{
    return ((int32_t)x < 0) ? (uint32_t)(UINT32_C(0) - x) : x;
}

static inline uint64_t sf_abs64(uint64_t x)
{
    return ((int64_t)x < 0) ? (uint64_t)(UINT64_C(0) - x) : x;
}

static inline uint8_t sf_usubsat8(uint8_t a, uint8_t b)
{
    return (a > b) ? (uint8_t)(a - b) : (uint8_t)0;
}

static inline uint16_t sf_usubsat16(uint16_t a, uint16_t b)
{
    return (a > b) ? (uint16_t)(a - b) : (uint16_t)0;
}

static inline uint32_t sf_usubsat32(uint32_t a, uint32_t b)
{
    return (a > b) ? (a - b) : UINT32_C(0);
}

static inline uint64_t sf_fshl64(uint64_t a, uint64_t b, uint64_t c)
{
    unsigned s = (unsigned)(c & 63);
    return s ? ((a << s) | (b >> (64 - s))) : a;
}

static inline uint32_t sf_fshl32(uint32_t a, uint32_t b, uint32_t c)
{
    unsigned s = (unsigned)(c & 31);
    return s ? ((a << s) | (b >> (32 - s))) : a;
}

/* ------------------------------------------------------ pinned poison -- */

static inline uint32_t sf_udiv32(uint32_t a, uint32_t b)
{
    return b ? (a / b) : UINT32_C(0);
}

static inline uint64_t sf_udiv64(uint64_t a, uint64_t b)
{
    return b ? (a / b) : UINT64_C(0);
}

/* ---------------------------------------------------------- 128-bit --- */

static inline sf_u128 sf_u128_of(uint64_t hi, uint64_t lo)
{
    return ((sf_u128)hi << 64) | (sf_u128)lo;
}
static inline uint64_t sf_u128_lo64(sf_u128 x) { return (uint64_t)x; }
static inline uint32_t sf_u128_lo32(sf_u128 x) { return (uint32_t)x; }
static inline uint16_t sf_u128_lo16(sf_u128 x) { return (uint16_t)x; }
static inline uint8_t sf_u128_lo8(sf_u128 x) { return (uint8_t)x; }
static inline bool sf_u128_lo1(sf_u128 x) { return (bool)(x & 1); }
static inline sf_u128 sf_u128_sext1(bool b)
{
    return b ? (sf_u128)0 - (sf_u128)1 : (sf_u128)0;
}
static inline sf_u128 sf_u128_sext64(uint64_t x)
{
    return (sf_u128)(sf_i128)(int64_t)x;
}
static inline sf_u128 sf_u128_and(sf_u128 a, sf_u128 b) { return a & b; }
static inline sf_u128 sf_u128_or(sf_u128 a, sf_u128 b) { return a | b; }
static inline sf_u128 sf_u128_xor(sf_u128 a, sf_u128 b) { return a ^ b; }
static inline sf_u128 sf_u128_add(sf_u128 a, sf_u128 b) { return a + b; }
static inline sf_u128 sf_u128_sub(sf_u128 a, sf_u128 b) { return a - b; }
static inline sf_u128 sf_u128_mul(sf_u128 a, sf_u128 b) { return a * b; }
static inline sf_u128 sf_u128_udiv(sf_u128 a, sf_u128 b)
{
    return b ? (a / b) : (sf_u128)0;
}
static inline sf_u128 sf_u128_shl(sf_u128 a, sf_u128 b)
{
    return a << (unsigned)(b & 127);
}
static inline sf_u128 sf_u128_lshr(sf_u128 a, sf_u128 b)
{
    return a >> (unsigned)(b & 127);
}
static inline bool sf_u128_eq(sf_u128 a, sf_u128 b) { return a == b; }
static inline int sf_u128_ucmp(sf_u128 a, sf_u128 b)
{
    return (a < b) ? -1 : ((a > b) ? 1 : 0);
}
static inline int sf_u128_scmp(sf_u128 a, sf_u128 b)
{
    sf_i128 x = (sf_i128)a, y = (sf_i128)b;
    return (x < y) ? -1 : ((x > y) ? 1 : 0);
}

#include "sfemul_decls.h"

#endif /* SFEMUL_H */
