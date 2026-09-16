// probe 636 -- binary <=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_636(bool a, int32_t b)
{
    return a <= b;
}
