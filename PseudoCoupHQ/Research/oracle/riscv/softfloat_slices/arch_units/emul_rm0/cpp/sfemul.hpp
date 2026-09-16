// sfemul.hpp - the eight LLVM intrinsics the flattened slices use, plus the
// three don't-care pins, written once for C++ and reused by every operation.
//
// ctlz       BUILT-IN: std::countl_zero (C++20) answers the bit width for 0,
//            which is exactly LLVM's ctlz with is_zero_poison=false, so the
//            edge case matches and the built-in is used.
// abs        WRITTEN OUT.  std::abs is undefined at INT_MIN; LLVM's llvm.abs
//            with is_int_min_poison=false wraps to INT_MIN.
// usub.sat   WRITTEN OUT.  C++ has no saturating subtract before C++26.
// fshl       WRITTEN OUT.  C++ has no funnel shift (std::rotl is a1 == b).
// udiv       WRITTEN OUT with a zero guard.
#ifndef SFEMUL_HPP
#define SFEMUL_HPP

#include <cstdint>
#include <bit>

namespace sfemul {

using sf_u128 = unsigned __int128;
using sf_i128 = signed __int128;

// ----------------------------------------------------------- intrinsics --

inline uint32_t sf_ctlz32(uint32_t x)
{
    return static_cast<uint32_t>(std::countl_zero(x));
}

inline uint64_t sf_ctlz64(uint64_t x)
{
    return static_cast<uint64_t>(std::countl_zero(x));
}

inline uint16_t sf_abs16(uint16_t x)
{
    return (static_cast<int16_t>(x) < 0)
        ? static_cast<uint16_t>(0u - static_cast<unsigned>(x)) : x;
}

inline uint32_t sf_abs32(uint32_t x)
{
    return (static_cast<int32_t>(x) < 0) ? static_cast<uint32_t>(0u - x) : x;
}

inline uint64_t sf_abs64(uint64_t x)
{
    return (static_cast<int64_t>(x) < 0)
        ? static_cast<uint64_t>(UINT64_C(0) - x) : x;
}

inline uint8_t sf_usubsat8(uint8_t a, uint8_t b)
{
    return (a > b) ? static_cast<uint8_t>(a - b) : static_cast<uint8_t>(0);
}

inline uint16_t sf_usubsat16(uint16_t a, uint16_t b)
{
    return (a > b) ? static_cast<uint16_t>(a - b) : static_cast<uint16_t>(0);
}

inline uint32_t sf_usubsat32(uint32_t a, uint32_t b)
{
    return (a > b) ? (a - b) : UINT32_C(0);
}

inline uint64_t sf_fshl64(uint64_t a, uint64_t b, uint64_t c)
{
    unsigned s = static_cast<unsigned>(c & 63);
    return s ? ((a << s) | (b >> (64 - s))) : a;
}

inline uint32_t sf_fshl32(uint32_t a, uint32_t b, uint32_t c)
{
    unsigned s = static_cast<unsigned>(c & 31);
    return s ? ((a << s) | (b >> (32 - s))) : a;
}

// ------------------------------------------------------- pinned poison --

inline uint32_t sf_udiv32(uint32_t a, uint32_t b)
{
    return b ? (a / b) : UINT32_C(0);
}

inline uint64_t sf_udiv64(uint64_t a, uint64_t b)
{
    return b ? (a / b) : UINT64_C(0);
}

// ------------------------------------------------------------- 128-bit --

inline sf_u128 sf_u128_of(uint64_t hi, uint64_t lo)
{
    return (static_cast<sf_u128>(hi) << 64) | static_cast<sf_u128>(lo);
}
inline uint64_t sf_u128_lo64(sf_u128 x) { return static_cast<uint64_t>(x); }
inline uint32_t sf_u128_lo32(sf_u128 x) { return static_cast<uint32_t>(x); }
inline uint16_t sf_u128_lo16(sf_u128 x) { return static_cast<uint16_t>(x); }
inline uint8_t sf_u128_lo8(sf_u128 x) { return static_cast<uint8_t>(x); }
inline bool sf_u128_lo1(sf_u128 x) { return static_cast<bool>(x & 1); }
inline sf_u128 sf_u128_sext1(bool b)
{
    return b ? static_cast<sf_u128>(0) - static_cast<sf_u128>(1)
             : static_cast<sf_u128>(0);
}
inline sf_u128 sf_u128_sext64(uint64_t x)
{
    return static_cast<sf_u128>(
        static_cast<sf_i128>(static_cast<int64_t>(x)));
}
inline sf_u128 sf_u128_and(sf_u128 a, sf_u128 b) { return a & b; }
inline sf_u128 sf_u128_or(sf_u128 a, sf_u128 b) { return a | b; }
inline sf_u128 sf_u128_xor(sf_u128 a, sf_u128 b) { return a ^ b; }
inline sf_u128 sf_u128_add(sf_u128 a, sf_u128 b) { return a + b; }
inline sf_u128 sf_u128_sub(sf_u128 a, sf_u128 b) { return a - b; }
inline sf_u128 sf_u128_mul(sf_u128 a, sf_u128 b) { return a * b; }
inline sf_u128 sf_u128_udiv(sf_u128 a, sf_u128 b)
{
    return b ? (a / b) : static_cast<sf_u128>(0);
}
inline sf_u128 sf_u128_shl(sf_u128 a, sf_u128 b)
{
    return a << static_cast<unsigned>(b & 127);
}
inline sf_u128 sf_u128_lshr(sf_u128 a, sf_u128 b)
{
    return a >> static_cast<unsigned>(b & 127);
}
inline bool sf_u128_eq(sf_u128 a, sf_u128 b) { return a == b; }
inline int sf_u128_ucmp(sf_u128 a, sf_u128 b)
{
    return (a < b) ? -1 : ((a > b) ? 1 : 0);
}
inline int sf_u128_scmp(sf_u128 a, sf_u128 b)
{
    sf_i128 x = static_cast<sf_i128>(a), y = static_cast<sf_i128>(b);
    return (x < y) ? -1 : ((x > y) ? 1 : 0);
}

}  // namespace sfemul

#include "sfemul_decls.hpp"

#endif  // SFEMUL_HPP
