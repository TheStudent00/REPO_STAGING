// probe 476 -- binary ==
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_476(uint64_t a, uint64_t b)
{
    return a == b;
}
