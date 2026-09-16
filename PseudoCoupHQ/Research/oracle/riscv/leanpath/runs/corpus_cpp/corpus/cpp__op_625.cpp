// probe 625 -- binary <=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_625(float a, int64_t b)
{
    return a <= b;
}
