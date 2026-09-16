// probe 657 -- binary <
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_657(uint64_t a, float b)
{
    return a < b;
}
