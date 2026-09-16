// probe 337 -- binary &&
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_337(float a, int64_t b)
{
    return a && b;
}
