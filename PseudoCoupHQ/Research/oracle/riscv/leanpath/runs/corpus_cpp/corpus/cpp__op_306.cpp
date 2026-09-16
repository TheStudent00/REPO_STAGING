// probe 306 -- binary ||
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_306(double a, int32_t b)
{
    return a || b;
}
