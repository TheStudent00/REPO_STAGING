// probe 363 -- binary |
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_363(int64_t a, float b)
{
    return a | b;
}
