// probe 680 -- binary <<
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_680(int32_t a, uint64_t b)
{
    return a << b;
}
