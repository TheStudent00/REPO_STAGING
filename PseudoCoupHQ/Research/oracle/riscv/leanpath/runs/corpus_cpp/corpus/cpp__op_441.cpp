// probe 441 -- binary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_441(uint64_t a, float b)
{
    return a & b;
}
