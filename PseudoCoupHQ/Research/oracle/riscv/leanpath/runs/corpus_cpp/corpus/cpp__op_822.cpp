// probe 822 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_822(int32_t a, int32_t b)
{
    return a and b;
}
