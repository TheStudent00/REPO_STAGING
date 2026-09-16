// probe 374 -- binary |
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_374(float a, uint64_t b)
{
    return a | b;
}
