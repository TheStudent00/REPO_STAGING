// probe 440 -- binary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_440(uint64_t a, uint64_t b)
{
    return a & b;
}
