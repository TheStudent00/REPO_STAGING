// probe 300 -- binary ||
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_300(float a, int32_t b)
{
    return a || b;
}
