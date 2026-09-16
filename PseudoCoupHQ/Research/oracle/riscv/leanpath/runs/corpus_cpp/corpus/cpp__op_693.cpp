// probe 693 -- binary <<
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_693(uint64_t a, float b)
{
    return a << b;
}
