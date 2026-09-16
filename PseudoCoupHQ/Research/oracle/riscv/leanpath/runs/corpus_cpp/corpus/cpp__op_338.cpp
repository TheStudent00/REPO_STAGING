// probe 338 -- binary &&
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_338(float a, uint64_t b)
{
    return a && b;
}
