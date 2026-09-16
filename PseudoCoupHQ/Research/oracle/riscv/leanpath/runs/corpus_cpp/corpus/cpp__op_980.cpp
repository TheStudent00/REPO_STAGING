// probe 980 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_980(uint64_t a, uint64_t b)
{
    return a not_eq b;
}
