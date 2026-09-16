// probe 606 -- binary <=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_606(int32_t a, int32_t b)
{
    return a <= b;
}
