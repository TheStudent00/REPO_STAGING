// probe 538 -- binary >
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_538(int32_t a, double b)
{
    return a > b;
}
