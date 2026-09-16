// probe 348 -- binary &&
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_348(bool a, int32_t b)
{
    return a && b;
}
