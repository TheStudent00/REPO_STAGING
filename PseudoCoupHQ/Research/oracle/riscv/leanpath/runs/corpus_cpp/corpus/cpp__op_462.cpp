// probe 462 -- binary ==
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_462(int32_t a, int32_t b)
{
    return a == b;
}
