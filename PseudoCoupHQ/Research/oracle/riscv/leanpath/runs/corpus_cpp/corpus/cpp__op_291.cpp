// probe 291 -- binary ||
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_291(int64_t a, float b)
{
    return a || b;
}
