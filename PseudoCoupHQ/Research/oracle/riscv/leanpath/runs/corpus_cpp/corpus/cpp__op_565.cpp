// probe 565 -- binary >
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_565(bool a, int64_t b)
{
    return a > b;
}
