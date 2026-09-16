// probe 324 -- binary &&
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_324(int64_t a, int32_t b)
{
    return a && b;
}
