// probe 698 -- binary <<
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_698(float a, uint64_t b)
{
    return a << b;
}
