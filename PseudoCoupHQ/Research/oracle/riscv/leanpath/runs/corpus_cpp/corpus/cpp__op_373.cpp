// probe 373 -- binary |
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_373(float a, int64_t b)
{
    return a | b;
}
