// probe 481 -- binary ==
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_481(float a, int64_t b)
{
    return a == b;
}
