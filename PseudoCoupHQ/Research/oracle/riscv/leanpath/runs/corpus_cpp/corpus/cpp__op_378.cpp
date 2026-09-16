// probe 378 -- binary |
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_378(double a, int32_t b)
{
    return a | b;
}
