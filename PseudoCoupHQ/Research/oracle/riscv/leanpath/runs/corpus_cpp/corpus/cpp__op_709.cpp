// probe 709 -- binary <<
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_709(bool a, int64_t b)
{
    return a << b;
}
