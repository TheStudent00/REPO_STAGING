// probe 564 -- binary >
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_564(bool a, int32_t b)
{
    return a > b;
}
