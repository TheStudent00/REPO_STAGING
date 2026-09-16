// probe 559 -- binary >
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_559(double a, int64_t b)
{
    return a > b;
}
